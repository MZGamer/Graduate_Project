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

GPTCall = GPTCall(OPENAIAPI, defTest)
googleAPI = googleAPI(GOOGLECLOUDAPI, SEARCHENGINEID, TOOFARDIST, defTest)
DB = DB(file_path, defTest)
restaurantListGenerator = restaurantListGenerator(googleAPI, GPTCall, DB, defTest)
restaurantListGenerator.task("嘉義市", "咖哩", RESTAURANTNEED, RANDOMNEED)