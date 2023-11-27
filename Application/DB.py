import random
from restaurant import Restaurant

from dataclasses import dataclass
from dataclasses import field
import pandas as pd
import csv

@dataclass
class DB:
    DB: pd.DataFrame
    DBPath: str
    defTest: bool

    def __init__(self, DBPath, defTest = False):
        self.DBPath = DBPath
        self.DB = pd.read_csv(DBPath)
        self.defTest = defTest
    def searchDB(self, restaurant_list):
        print("-----------------Checking DB-----------------")
        chkedRestaurant = []
        needChkRestaurant = []
        for restaurantName in restaurant_list:
            indexList = self.DB.index[self.DB["Name"] == restaurantName].tolist()
            if len(indexList) != 0:
                restaurantData = self.DB.loc[indexList[0]]
                if(self.defTest):
                    print(f"restaurant: {restaurantName} in DB")
                loc = restaurantData["location"].split(",")
                location = {'lat': loc[0], 'lng': loc[1]}
                chkedRestaurant.append(Restaurant(restaurantData["Name"], restaurantData["placeID"], restaurantData["type"], restaurantData["address"], location, restaurantData["command"], restaurantData["rating"], restaurantData["userRatingTotal"], self.scoreAnalyze(restaurantData["detailRating"])))
            else:
                if(self.defTest):
                    print(f"restaurant: {restaurantName} NOT in DB")
                needChkRestaurant.append(Restaurant(restaurantName))

        return chkedRestaurant, needChkRestaurant
    

    def randomSelect(self, restaurant_list, needed):
        print("-----------------Random Select-----------------")
        predToType = {0: '飲料',1: '甜點',2: '港式',3: '韓式',4: '歐美',5: '素食',6: '東南亞',7: '中式',8: '健康餐',9: '台式',10: '日式',11: '小吃'}
        inv_label_dict = {v: k for k, v in predToType.items()}
        currentList = [0,0,0,0,0,0,0,0,0,0,0,0]
        if(len(restaurant_list) >= needed):
            return restaurant_list
        
        for r in restaurant_list:
            if(type(r.type) != str):
                continue
            print(r.type)
            print(inv_label_dict[r.type])
            print()
            currentList[inv_label_dict[r.type]] += 1

        while(len(restaurant_list) < needed or sum(currentList) < needed):
            print(sum(currentList))
            print(needed)
            for i in range(len(currentList)):
                if(currentList[i] > min(currentList)):
                    continue
                fliter1 = (self.DB["type"] == predToType[i])
                fliter2 = (self.DB["rating"] > 4)
                res = self.DB[fliter1 & fliter2].index
                if(len(res) == 0):
                    currentList[i]+= 1
                    continue
                else:
                    success = False
                    for retryCounter in range(3):
                        select = random.randint(0, len(res)-1)
                        restaurantData = self.DB.loc[res[select]]
                        loc = restaurantData["location"].split(",")
                        location = {'lat': loc[0], 'lng': loc[1]}
                        selectRestaurant = (Restaurant(restaurantData["Name"], restaurantData["placeID"], restaurantData["type"], restaurantData["address"], location, restaurantData["command"], restaurantData["rating"], restaurantData["userRatingTotal"], self.scoreAnalyze(restaurantData["detailRating"])))
                        if (selectRestaurant in restaurant_list):
                            continue
                        else:
                            restaurant_list.append(selectRestaurant)
                            currentList[i]+= 1
                            success = True
                            print(f"choose: {restaurantData['Name']}")
                            break
                    if(success == False):
                        currentList[i]+= 1
        return restaurant_list





    def scoreAnalyze(self, scoreString):
        scoreString = scoreString.split(",")
        score = []
        for s in scoreString:
            score.append(float(s))
        return score
    
    def DBAddRestaurant(self, restaurantList):
        
        with open('restaurantDB.csv', 'a', newline='', encoding='utf-8') as file:
            for r in restaurantList:
                location = f"{r.location['lat']},{r.location['lng']}"
                detailRating = f"{r.detailRating[0]},{r.detailRating[1]},{r.detailRating[2]},{r.detailRating[3]},{r.detailRating[4]}"
                writer = csv.writer(file)
                writer.writerow([r.name, r.placeID, r.address,location,r.GRating,r.raitingTotal,r.review,detailRating,r.type, r.command])
        file.close()
        self.reloadDB()

    def reloadDB(self):
        self.DB = pd.read_csv(self.DBPath)



