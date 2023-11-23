from dataclasses import dataclass
from dataclasses import field
from googleAPI import googleAPI
from GPTCall import GPTCall
from DB import DB
from reviewGetter import getReview
from transformerModel import transformerModel

@dataclass
class restaurantListGenerator:
    googleAPI: googleAPI
    GPTCall: GPTCall
    DB: DB
    PEREXTRACT: int
    defTest: bool
    model: transformerModel


    def __init__(self, googleAPI, GPTCall, DB, model, defTest = False):
        self.googleAPI = googleAPI
        self.GPTCall = GPTCall
        self.DB = DB
        self.PEREXTRACT = 3
        self.defTest = defTest
        self.model = model

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
    

    def task(self, userPoint, target, restaurantNeeded, randomNeeded = 0):
        startPoint = 0
        randomRestaurantCount = 0
        restaurant_list = []
        DBBuildingList = []
        """r = self.googleAPI.googleSearch(question= userPoint + target)
        searchResult = self.googleAPI.searchResultExtract(r)

        #Random Restaurant
        if (target == "美食"):
            GPTResponse=(self.GPTCall.restaurantGenerate(userPoint, 0, randomNeeded))
            nameChkedRestaurantList = self.GPT_restaurant_list_Analyze(GPTResponse)
            
            existRestaurant_list, needChkRestaurantList = self.DB.searchDB(nameChkedRestaurantList)
            restaurant_list.extend(self.googleAPI.distChk(userPoint,existRestaurant_list))

            chkedRestaurantList = self.googleAPI.chkRestaurantInfo(userPoint,needChkRestaurantList)
            chkedRestaurantList = self.googleAPI.distChk(userPoint,chkedRestaurantList)
            DBBuildingList.extend(chkedRestaurantList)

            randomRestaurantCount = len(restaurant_list)"""
        while(startPoint <= 10):

            #GPTResponse= (self.GPTCall.restaurantGenerate(userPoint, 1, restaurantNeeded, searchResult,startPoint, self.PEREXTRACT))
            GPTResponse="1. 大雅牛排"
            inp = input("checkPoint Enter exit to stop ,other to continue")

            if(inp == "exit"):
                break

            nameChkedRestaurantList = self.GPT_restaurant_list_Analyze(GPTResponse)
            

            existRestaurant_list, needChkRestaurantList = self.DB.searchDB(nameChkedRestaurantList)
            restaurant_list.extend(self.googleAPI.distChk(userPoint,existRestaurant_list))

            chkedRestaurantList = self.googleAPI.chkRestaurantInfo(userPoint,needChkRestaurantList)
            chkedRestaurantList = self.googleAPI.distChk(userPoint,chkedRestaurantList)
            DBBuildingList.extend(chkedRestaurantList)

            if(len(restaurant_list) - randomRestaurantCount >= restaurantNeeded):
                break

            startPoint += self.PEREXTRACT
            print("-----------------A TURN COMPLETE-----------------")
            print(f"Current len of List : {len(restaurant_list)}")
            if(self.defTest):
                inp = input("Enter exit to stop ,other to continue")

                if(inp == "exit"):
                    break

        print("-----------------Result IN DB-----------------")
        for restaurant in restaurant_list:
            restaurant.print()
            print()

        print("-----------------DB BUILDING-----------------")
        DBBuildingList = getReview([DBBuildingList[0]])
        for restaurant in DBBuildingList:
            forType, forReview, forFinal = self.model.textPreProcess(restaurant.review)
            restaurant.type = self.model.typePredict(forType)
            finalScore, reviewEachScore = self.model.reviewPredict(forReview)
            review = ""
            print(reviewEachScore)
            print(len(forFinal))
            print(len(reviewEachScore))
            print(len(reviewEachScore[0]))
            print(len(reviewEachScore[1]))
            print(len(reviewEachScore[2]))
            print(len(reviewEachScore[3]))
            print(len(reviewEachScore[4]))
            for i in range(len(forFinal)):
                if(i != 0):
                    review += "|"
                review += f"{reviewEachScore[0][i]},{reviewEachScore[1][i]},{reviewEachScore[2][i]},{reviewEachScore[3][i]},{reviewEachScore[4][i]}^{forFinal[i]}"
            restaurant.review = review
            restaurant.detailRating = finalScore
            
        self.DB.DBAddRestaurant(DBBuildingList)
        print("-----------------Tack Complete-----------------")




