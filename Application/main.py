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


GPTCall = GPTCall(OPENAIAPI, defTest)
googleAPI = googleAPI(GOOGLECLOUDAPI, SEARCHENGINEID, TOOFARDIST, defTest)
DB = DB(file_path, defTest)
model = transformerModel(modelPath, typeVersion, reviewVersion)
restaurantListGenerator = restaurantListGenerator(googleAPI, GPTCall, DB, model,defTest)


restaurantListGenerator.task("嘉義市", "咖哩", RESTAURANTNEED, RANDOMNEED)
"""
testCase = DB.DB["Review"][1]
forType, forReview = model.textPreProcess(testCase)
finalScore, reviewEachScore = model.reviewPredict(forReview)
print(finalScore)"""
#test = Restaurant("test", "test", "test", "test", {'lat': 1, 'lng': 2}, "", 0,0, [0,0,0,0,0], "")
#DB.DBAddRestaurant([test])
#"[3.0588235294117645, 4.0, 3.8461538461538463, 3.1666666666666665, 3.731132075471698]"穀谷