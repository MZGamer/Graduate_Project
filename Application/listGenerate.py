from dataclasses import dataclass
from dataclasses import field
from googleAPI import googleAPI
from GPTCall import GPTCall
from DB import DB
from reviewGetter import getReview

@dataclass
class restaurantListGenerator:
    googleAPI: googleAPI
    GPTCall: GPTCall
    DB: DB
    PEREXTRACT: int
    defTest: bool

    def __init__(self, googleAPI, GPTCall, DB, defTest = False):
        self.googleAPI = googleAPI
        self.GPTCall = GPTCall
        self.DB = DB
        self.PEREXTRACT = 3
        self.defTest = defTest

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
        r = self.googleAPI.googleSearch(question= userPoint + target)
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

            randomRestaurantCount = len(restaurant_list)
        while(startPoint <= 10):

            GPTResponse= (self.GPTCall.restaurantGenerate(userPoint, 1, restaurantNeeded, searchResult,startPoint, self.PEREXTRACT))
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
        DBBuildingList = getReview(DBBuildingList)
        for i in range(len(DBBuildingList)):
            print(DBBuildingList[i])
            print(f"review{DBBuildingList[i].review}")
            print()




