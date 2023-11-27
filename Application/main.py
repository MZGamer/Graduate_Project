#import
import requests
import json
import openai
import os
from dataclasses import dataclass
from dataclasses import field
import csv
import pandas as pd
from restaurant import Restaurant
from DB import DB
from googleAPI import googleAPI
from GPTCall import GPTCall
from DB import DB
from listGenerate import restaurantListGenerator
from transformerModel import transformerModel
from networkManager import server
from package import *
import json
import threading
#Test Panel
defTest = True

#CONST
GOOGLECLOUDAPI = "AIzaSyDn8Sz9ew_JmEiJuVPUsnL2delyY4wWgVU"
SEARCHENGINEID = "f5493b03adf724111"
OPENAIAPI = "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"
TOOFARDIST = 10000 #(公尺)
RESTAURANTNEED = 10
RANDOMNEED = 10
DATAPREEXTRACT = 3

#DB
file_path= './restaurantDB.csv'

#model
modelPath = "D:/Work/Project/School_Homework/Graduate_Project/predict_Model"
typeVersion = "1121"
reviewVersion = "1123"

#server
HOST = '127.0.0.1'
PORT = 2933
isConnected = False

def packageAnalyze(package : Package):
    if package.ACTION == ACTION.ASKGPT:
        threading.Thread(target=restaurantListGenerator.task, args=([package.requestLocation, package.requestTarget, package.restaurantNeed, package.randomNeed])).start()
    elif package.ACTION == ACTION.REQUESTRESTAURANT:
        restaurantListGenerator.restaurantRequest(package.restaurantRequestName)
    """else:
        return Package()"""
    
def scoreAnalyze( scoreString):
    scoreString = scoreString.split(",")
    score = []
    for s in scoreString:
        score.append(float(s))
    return score

GPTCall = GPTCall(OPENAIAPI, defTest)
googleAPI = googleAPI(GOOGLECLOUDAPI, SEARCHENGINEID, TOOFARDIST, defTest)
DB = DB(file_path, defTest)
print(DB.DB.index)
model = transformerModel(modelPath, typeVersion, reviewVersion)
server = server(HOST, PORT)
restaurantListGenerator = restaurantListGenerator(googleAPI, GPTCall, DB, model, server, defTest)

chkedRestaurant = []
indexList = DB.DB.index[DB.DB["Name"] == "大雅牛排"].tolist()
if len(indexList) != 0:
    restaurantData = DB.DB.loc[indexList[0]]
    if(defTest):
        print(f"restaurant: 八谷 豬排 咖哩 民族店 in DB")
    loc = restaurantData["location"].split(",")
    location = {'lat': loc[0], 'lng': loc[1]}
    chkedRestaurant.append(Restaurant(restaurantData["Name"], restaurantData["placeID"], restaurantData["type"], restaurantData["address"], location, restaurantData["command"], restaurantData["rating"], restaurantData["userRatingTotal"], scoreAnalyze(restaurantData["detailRating"]), restaurantData["Review"]))

chkedRestaurant[0].review = chkedRestaurant[0].review.replace("\n", "\\")
chkedRestaurant[0].review = chkedRestaurant[0].review.replace("\r", "\\")
test = Package(ACTION.RECEIVEDATA, "", "", "", chkedRestaurant)



isConnected = server.start()

server.sendPackage(test)
while True:
    if(isConnected == False):
        isConnected = server.start()
        server.sendPackage(test)

        continue
    pkg = server.listenPackage()
    if pkg == "close":
        isConnected = False
    elif pkg != None:
        packageAnalyze(pkg)


#restaurantListGenerator.task("嘉義市", "咖哩", RESTAURANTNEED, RANDOMNEED)
"""
testCase = DB.DB["Review"][1]
forType, forReview = model.textPreProcess(testCase)
finalScore, reviewEachScore = model.reviewPredict(forReview)
print(finalScore)"""
#test = Restaurant("test", "test", "test", "test", {'lat': 1, 'lng': 2}, "", 0,0, [0,0,0,0,0], "")
#DB.DBAddRestaurant([test])
#"[3.0588235294117645, 4.0, 3.8461538461538463, 3.1666666666666665, 3.731132075471698]"穀谷