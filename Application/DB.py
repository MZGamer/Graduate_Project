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



