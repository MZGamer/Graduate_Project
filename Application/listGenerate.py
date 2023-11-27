from dataclasses import dataclass
from dataclasses import field
from googleAPI import googleAPI
from GPTCall import GPTCall
from DB import DB
from reviewGetter import getReview
from transformerModel import transformerModel
from networkManager import server
from package import *
from reviewSelect import *
import copy
@dataclass
class restaurantListGenerator:
    googleAPI: googleAPI
    GPTCall: GPTCall
    DB: DB
    PEREXTRACT: int
    defTest: bool
    model: transformerModel
    server: server


    def __init__(self, googleAPI, GPTCall, DB, model, server, defTest = False):
        self.googleAPI = googleAPI
        self.GPTCall = GPTCall
        self.DB = DB
        self.PEREXTRACT = 3
        self.defTest = defTest
        self.model = model
        self.server = server


    def chkRepeat(self, restaurant_list):
        placeIDList = []
        noRepeatList = []
        for r in restaurant_list:
            if(r.placeID not in placeIDList):
                print(f"{r.placeID} | {placeIDList}")
                noRepeatList.append(r)
                placeIDList.append(r.placeID)
        return noRepeatList
    
    def GPT_restaurant_list_Analyze(self, GPTResponse):
        print("-----------------Starting Analyze Restaurant List from GPT-----------------")
        raw_restaurant_list = GPTResponse.split('\n')
        if(self.defTest):
            print(f"RawList:{raw_restaurant_list}")

        restaurant_name_list = []
        for item in raw_restaurant_list:
            item = item.strip()
            if(self.defTest):
                print(f"item:{item}")
            try:
                int(item[0])
            except:
                continue
            if(int(item[0]) >= int('0') and  int(item[0]) <= int('9')):
                splitPoint = 0
                if(self.defTest):
                    print(f"splitPoint:{splitPoint}")
                    print(f"find:{item.find('.',splitPoint+1)}")
                splitPoint = item.find('.',splitPoint)
                restaurant_name_list.append(item[splitPoint+2:])
        
        if(self.defTest):
            print(restaurant_name_list)

        nameChkedRestaurantList = self.googleAPI.restaurantNameCheck(restaurant_name_list)
        return nameChkedRestaurantList
    
    def restaurantRequest(self, restaurantName):
        nameChkedRestaurantList = self.googleAPI.restaurantNameCheck([restaurantName])
        existRestaurant_list, needChkRestaurantList = self.DB.searchDB(nameChkedRestaurantList)
        if (len(existRestaurant_list) != 0):
            package = Package(ACTION.RECEIVEDATA, "", "", "", existRestaurant_list)
            self.server.sendPackage(package)
            return
        else:
            print("-----------------DB BUILDING-----------------")
            needChkRestaurantList = self.googleAPI.chkRestaurantInfo("",needChkRestaurantList)
            DBBuildingList = getReview(needChkRestaurantList)
            for restaurant in DBBuildingList:
                forType, forReview, forFinal = self.model.textPreProcess(restaurant.review)
                restaurant.type = self.model.typePredict(forType)
                finalScore, reviewEachScore = self.model.reviewPredict(forReview)
                review = ""
                for i in range(len(forFinal)):
                    if(i != 0):
                        review += "|"
                    review += f"{reviewEachScore[0][i]},{reviewEachScore[1][i]},{reviewEachScore[2][i]},{reviewEachScore[3][i]},{reviewEachScore[4][i]}^{forFinal[i]}"
                restaurant.review = review
                restaurant.detailRating = finalScore

                reviewListWithScore = reviewPreprocess(restaurant)
                pendingList = reviewClassify(reviewListWithScore)
                reviewPicked = reviewPick(pendingList)
                r = self.GPTCall.sendGPTRequest("", 2, 0, [], 0, 0, restaurant, reviewPicked)
                restaurant.command = r.replace("*", "")
            restaurantSend = copy.deepcopy(DBBuildingList)
            package = Package(ACTION.RECEIVEDATA, "", "", "", restaurantSend)
            self.server.sendPackage(package)            
            self.DB.DBAddRestaurant(DBBuildingList)
            print("-----------------Tack Complete-----------------")




    def task(self, userPoint, target, restaurantNeeded, randomNeeded = 0):
        startPoint = 0
        randomRestaurantCount = 0
        restaurant_list = []
        DBBuildingList = []
        r = self.googleAPI.googleSearch(question= userPoint + target, need = max(restaurantNeeded, 10))
        searchResult = self.googleAPI.searchResultExtract(r)

        #Random Restaurant
        if (target == "美食"):
            GPTResponse=(self.GPTCall.sendGPTRequest(userPoint, 0, randomNeeded))
            nameChkedRestaurantList = self.GPT_restaurant_list_Analyze(GPTResponse)
            
            existRestaurant_list, needChkRestaurantList = self.DB.searchDB(nameChkedRestaurantList)
            restaurant_list.extend(self.googleAPI.distChk(userPoint,existRestaurant_list))

            chkedRestaurantList = self.googleAPI.chkRestaurantInfo(userPoint,needChkRestaurantList)
            chkedRestaurantList = self.googleAPI.distChk(userPoint,chkedRestaurantList)
            DBBuildingList.extend(chkedRestaurantList)

            randomRestaurantCount = len(restaurant_list)
        while(startPoint < len(searchResult)):
            """
            inp = input("checkPoint Enter exit to stop ,other to continue")
            if(inp == "exit"):
                break"""
            GPTResponse= (self.GPTCall.sendGPTRequest(userPoint, 1, restaurantNeeded, searchResult,startPoint, self.PEREXTRACT))
            



            nameChkedRestaurantList = self.GPT_restaurant_list_Analyze(GPTResponse)
            

            existRestaurant_list, needChkRestaurantList = self.DB.searchDB(nameChkedRestaurantList)
            distChkedRestaurantList = self.googleAPI.distChk(userPoint,existRestaurant_list)
            restaurant_list.extend(distChkedRestaurantList)

            chkedRestaurantList = self.googleAPI.chkRestaurantInfo(userPoint,needChkRestaurantList)
            chkedRestaurantList = self.googleAPI.distChk(userPoint,chkedRestaurantList)
            DBBuildingList.extend(chkedRestaurantList)

            if(len(restaurant_list) - randomRestaurantCount >= restaurantNeeded):
                break

            startPoint += self.PEREXTRACT

            restaurant_list = self.chkRepeat(restaurant_list)
            DBBuildingList = self.chkRepeat(DBBuildingList)
            print("-----------------A TURN COMPLETE-----------------")
            print(f"Current len of List : {len(restaurant_list)}")
            if(self.defTest):
                """
                inp = input("Enter exit to stop ,other to continue")

                if(inp == "exit"):
                    break
                    """
        if(target == "美食"):
            restaurant_list = self.DB.randomSelect(restaurant_list, restaurantNeeded + randomNeeded)
        print("-----------------Result IN DB-----------------")
        restaurant_list = self.chkRepeat(restaurant_list)
        DBBuildingList = self.chkRepeat(DBBuildingList)
        for restaurant in restaurant_list:
            restaurant.print()
            print()
        package = Package(ACTION.RECEIVEDATA, "", "", "", restaurant_list)
        self.server.sendPackage(package)

        print("-----------------DB BUILDING-----------------")
        DBBuildingList = getReview(DBBuildingList)
        for restaurant in DBBuildingList:
            forType, forReview, forFinal = self.model.textPreProcess(restaurant.review)
            restaurant.type = self.model.typePredict(forType)
            finalScore, reviewEachScore = self.model.reviewPredict(forReview)
            review = ""
            """
            print(reviewEachScore)
            print(len(forFinal))
            print(len(reviewEachScore))
            print(len(reviewEachScore[0]))
            print(len(reviewEachScore[1]))
            print(len(reviewEachScore[2]))
            print(len(reviewEachScore[3]))
            print(len(reviewEachScore[4]))"""
            for i in range(len(forFinal)):
                if(i != 0):
                    review += "|"
                review += f"{reviewEachScore[0][i]},{reviewEachScore[1][i]},{reviewEachScore[2][i]},{reviewEachScore[3][i]},{reviewEachScore[4][i]}^{forFinal[i]}"
            restaurant.review = review
            restaurant.detailRating = finalScore
            reviewListWithScore = reviewPreprocess(restaurant)
            pendingList = reviewClassify(reviewListWithScore)
            reviewPicked = reviewPick(pendingList)
            r = self.GPTCall.sendGPTRequest("", 2, 0, [], 0, 0, restaurant, reviewPicked)
            restaurant.command = r.replace("*", "")
             
        self.DB.DBAddRestaurant(DBBuildingList)
        print("-----------------Tack Complete-----------------")




