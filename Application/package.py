import base64
from enum import IntEnum
from dataclasses import dataclass
from dataclasses import field

import numpy as np
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
    
    def obj2Json(package):
        print(package)
        if (type(package) == Restaurant):
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
                "review" : package.review
            }
        elif (type(package) == Package):
            return {
                "ACTION" : package.ACTION,
                "restaurantRequestName" : package.restaurantRequestName,
                "requestLocation" : package.requestLocation,
                "requestTarget" : package.requestTarget,
                "restaurantData" : package.restaurantData
            }
        else:
            pass

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def __init__(self, ACTION = ACTION.RECEIVEDATA,restaurantRequestName = "",requestLocation = "",requestTarget = "", restaurantData = []):
        self.ACTION = ACTION
        self.restaurantData = restaurantData
        self.restaurantRequestName = restaurantRequestName
        self.requestLocation = requestLocation
        self.requestTarget = requestTarget

