from restaurant import Restaurant

from dataclasses import dataclass
from dataclasses import field
import pandas as pd

@dataclass
class DB:
    DB: pd.DataFrame
    defTest: bool

    def __init__(self, DBPath, defTest = False):
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
                chkedRestaurant.append(Restaurant(restaurantData["Name"], restaurantData["placeID"], restaurantData["label"], restaurantData["address"], location, restaurantData["command"], restaurantData["rating"], restaurantData["userRatingTotal"], restaurantData["detailRating"]))
            else:
                if(self.defTest):
                    print(f"restaurant: {restaurantName} NOT in DB")
                needChkRestaurant.append(Restaurant(restaurantName))

        return chkedRestaurant, needChkRestaurant



