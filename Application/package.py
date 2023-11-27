import base64
from enum import IntEnum
from dataclasses import dataclass
from dataclasses import field

from restaurant import Restaurant
import json

class ACTION(IntEnum):
    NULL = 0
    RECEIVEDATA = 1
    ASKGPT = 2
    REQUESTRESTAURANT = 3


class Package:
    ACTION : ACTION = ACTION.NULL
    restaurantRequestName : str = ""
    requestLocation : str = ""
    requestTarget : str = ""
    restaurantData : list[Restaurant] = []
    restaurantNeed : int
    randomNeed : int
    
    def obj2Json(package):
        if (type(package) == Restaurant):
            if type(package.command) != str:
                package.command = ""
            else:
                package.command = package.command.replace("\n", "/n").replace("\r", "/n")

            if type(package.review) != str:
                package.review = ""
            else:
                package.review = package.review.replace("\n", "/n").replace("\r", "/n")
            return {
                "name" : package.name,
                "placeID" : package.placeID,
                "type" : package.type,
                "address" : package.address,
                "location" : package.location,
                "command" : package.command,
                "GRating" : package.GRating,
                "raitingTotal" : package.raitingTotal,
                "detailRating" : package.detailRating,
                "review" : package.review.replace("\n", "\\").replace("\r", "\\")
            }
        elif (type(package) == Package):
            return {
                "ACTION" : package.ACTION,
                "restaurantRequestName" : package.restaurantRequestName,
                "requestLocation" : package.requestLocation,
                "requestTarget" : package.requestTarget,
                "restaurantData" : package.restaurantData,
                "restaurantNeed" : package.restaurantNeed,
                "randomNeed" : package.randomNeed
            }
        else:
            pass

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def __init__(self, ACTION = ACTION.RECEIVEDATA,restaurantRequestName = "",requestLocation = "",requestTarget = "", restaurantData = [], restaurantNeed = 0, randomNeed = 0):
        self.ACTION = ACTION
        self.restaurantData = restaurantData
        self.restaurantRequestName = restaurantRequestName
        self.requestLocation = requestLocation
        self.requestTarget = requestTarget
        self.restaurantNeed = restaurantNeed
        self.randomNeed = randomNeed

