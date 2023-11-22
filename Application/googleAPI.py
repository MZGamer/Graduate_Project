from restaurant import Restaurant
import requests
from dataclasses import dataclass
from dataclasses import field
import pandas as pd
import json

@dataclass
class googleAPI:
    GOOGLECLOUDAPI: str
    SEARCHENGINEID: str
    TOOFARDIST: int
    defTest: bool

    def __init__(self, GOOGLECLOUDAPI, SEARCHENGINEID, TOOFARDIST, defTest = False):
        self.GOOGLECLOUDAPI = GOOGLECLOUDAPI
        self.SEARCHENGINEID = SEARCHENGINEID
        self.TOOFARDIST = TOOFARDIST
        self.defTest = defTest

    def googleSearch(self, question):
        print("-----------------Searching Data with googleSearch-----------------")
        googleAPIkey = "key=" + self.GOOGLECLOUDAPI
        searchEngineID = "&cx=" + self.SEARCHENGINEID
        query = "&q=" + question
        searchAPI = "https://www.googleapis.com/customsearch/v1?" 

        reauestURL = searchAPI + googleAPIkey + searchEngineID + query
        r = requests.get(reauestURL)
        if(self.defTest):
            print(f"return status : {r}")
        return r
    
    def searchResultExtract(self, r, defTest = False):
        searchResult = []
        out = json.loads(r.text)
        for i in out["items"]:
            if(self.defTest):
                print(i["snippet"])
            searchResult.append(i["snippet"])
        if(self.defTest):
            print(f"Result len : {len(searchResult)}")
        return searchResult
    
    def restaurantNameCheck(self, nameChkRestaurantList):
        nameChkedRestaurantList = []
        for name in nameChkRestaurantList:
            gapi = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
            query = "?input=" + name#
            inputtype = "&inputtype=textquery"
            detail = "&language=zh-TW"
            fields = "&fields=name"
            loc = "&locationbias=circle:10000@23.4800751,120.4491113"
            key = "&key=" + self.GOOGLECLOUDAPI
            requestsURL = gapi + query +inputtype + loc + detail + key + fields

            # 使用 GET 方式下載普通網頁
            r = requests.get(requestsURL)
            if(self.defTest):
                print(r)

            out = json.loads(r.text)
            if (out['status'] == 'ZERO_RESULTS'):
                continue
            realName = out['candidates'][0]['name']
            if(realName not in nameChkedRestaurantList):
                nameChkedRestaurantList.append(realName)
        
        return nameChkedRestaurantList

    def chkRestaurantInfo(self, userPoint,needChkRestaurantList):
        print("-----------------Search Restaurant Data with googleMap-----------------")
        existRestaurantList = []
        for restaurant in needChkRestaurantList:
            gapi = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            query = "?query=" + userPoint + restaurant.name
            detail = "&language=zh-TW"
            key = "&key=" + self.GOOGLECLOUDAPI
            requestsURL = gapi + query + detail + key
            
            # 使用 GET 方式下載普通網頁
            r = requests.get(requestsURL)
            if(self.defTest):
                print(r)

            out = json.loads(r.text)
            placeData = out['results']
            print(placeData)
            if(len(placeData) == 0):
                continue
            
            restaurantName = placeData[0]["name"]
            placeID = placeData[0]["place_id"]
            formatted_address = placeData[0]["formatted_address"]
            location = placeData[0]["geometry"]["location"]
            rating = placeData[0]["rating"]
            userRatingTotal = placeData[0]["user_ratings_total"]

            existRestaurantList.append(Restaurant(restaurantName, placeID, "", formatted_address, location, "", rating , userRatingTotal))

            if(self.defTest):
                print("restaurantData:")
                print(f"find len{len(placeData)}")
                print(placeData[0].keys())
                print(f"Name: {restaurantName}")
                print(f"placeID: {placeID}")
                print(f"address: {formatted_address}")
                print(f"location: {location}")
                print(f"rating: {rating}")
                print(f"userRatingTotal: {userRatingTotal}")
                print()

        return existRestaurantList

    def distChk(self, userPoint, distChkRestaurantList):
        print("-----------------Checking Dist with googleMap-----------------")
        originPoint = "Taiwan " + userPoint
        nearRestaurantList = []
        for restaurant in distChkRestaurantList:
            destinationPoint = "place_id:" + restaurant.placeID
            #Place your google map API_KEY to a variable
            apiKey = self.GOOGLECLOUDAPI
            #Store google maps api url in a variable
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
            # call get method of request module and store respose object
            #print(url + 'origins=' + originPoint + '&destinations=' + destinationPoint + '&key=' + apiKey)
            r = requests.get(url + 'origins=' + originPoint + '&destinations=' + destinationPoint + '&key=' + apiKey)
            #Get json format result from the above response object
            res = r.json()

            if(self.defTest):
                print(r.json())
            statusCode = res['rows'][0]['elements'][0]['status']
            if(statusCode == 'ZERO_RESULTS' or statusCode == 'NOT_FOUND'):
                if(self.defTest):
                    print(f"restaurant: {restaurant.name} is too far")
                continue
            
            #print the value of res
            dist = res["rows"][0]["elements"][0]['distance']['value']
            if(self.defTest):
                print(dist)
            if(dist <= self.TOOFARDIST):
                nearRestaurantList.append(restaurant)
        
        return nearRestaurantList
            
