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
GOOGLECLOUDAPI = "APIKEY"
SEARCHENGINEID = "APIKEY"
OPENAIAPI = "APIKEY"
TOOFARDIST = 10000 #(公尺)
RESTAURANTNEED = 10
RANDOMNEED = 10
DATAPREEXTRACT = 3

#DB
file_path= './restaurantDB.csv'

#model
modelPath = "D:/Work/Project/School_Homework/Graduate_Project/predict_Model"
typeVersion = "1121"
reviewVersion = "1127"

#server
HOST = '25.33.153.168'
PORT = 2933
isConnected = False

def packageAnalyze(package : Package):
    try:
        if package.ACTION == ACTION.ASKGPT:
            threading.Thread(target=restaurantListGenerator.task, args=([package.requestLocation, package.requestTarget, package.restaurantNeed, package.randomNeed])).start()
        elif package.ACTION == ACTION.REQUESTRESTAURANT:
            restaurantListGenerator.restaurantRequest(package.restaurantRequestName)
    except Exception as e:
        print(e)
        errorpkg = Package(ACTION.RECEIVEDATA, "", "", "", errorMessage)
        server.sendPackage(errorpkg)
        return
    """else:
        return Package()"""
    


errorMessage = Restaurant("Error", "", "", "Please Check server log")
GPTCall = GPTCall(OPENAIAPI, defTest)
googleAPI = googleAPI(GOOGLECLOUDAPI, SEARCHENGINEID, TOOFARDIST, defTest)
DB = DB(file_path, defTest)
print(DB.DB.index)
model = transformerModel(modelPath, typeVersion, reviewVersion)
server = server(HOST, PORT)
restaurantListGenerator = restaurantListGenerator(googleAPI, GPTCall, DB, model, server, defTest)



isConnected = server.start()


while True:
    if(isConnected == False):
        isConnected = server.start()

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
