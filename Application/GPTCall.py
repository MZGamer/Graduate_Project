from restaurant import Restaurant
import requests
from dataclasses import dataclass
from dataclasses import field
import pandas as pd
import json
import openai

@dataclass
class GPTCall:
    OPENAIAPI = str
    TOOFARDIST = 10000 #(公尺)
    RESTAURANTNEED = int
    RANDOMNEED = int
    DATAPREEXTRACT = int
    defTest: bool
    def __init__(self, OPENAIAPI, defTest = False):
        self.OPENAIAPI = OPENAIAPI
        self.defTest = defTest
    def messageGenerate(self, place, mode, needed, searchResult = [], startPoint = 0, perExtract = 0):
        if mode == 0:
            sendMessage =[
                {"role": "system", "content": "你是一個美食評論公司的助理，你的任務是根據你的記憶，來提供要交給美食評論家去光顧的店家，回答的規則如下"},
                {"role": "assistant", "content": "1. 所有的餐廳名稱須依順序加上編號，範例: 1. 餐廳名稱\n 2. 餐廳名稱"},
                {"role": "assistant", "content": f"2. 餐廳的數量上限為{min(10,needed)}間 "},
                {"role": "assistant", "content": f"3. 請提供{needed}間餐廳 "},
                {"role": "assistant", "content": "以下為範例"},
                {"role": "assistant", "content": "Q: 安南市"},
                {"role": "assistant", "content": "Ans:"},
                {"role": "assistant", "content": "1. 阿財羊肉爐"},
                {"role": "assistant", "content": "2. 好喝豆漿"},
                {"role": "assistant", "content": "3. 洪記牛肉麵"},
                {"role": "assistant", "content": "4. 凱霞牛肉湯"},
                {"role": "assistant", "content": f"\n 接下來我會給你地點"},
                {"role": "assistant", "content": f"請依照你的記憶提供餐廳名單"},
                {"role": "assistant", "content": f"Q:台灣{place}"}
            ]
            return sendMessage
        else:
            sendMessage =[
                {"role": "system", "content": "你是一個美食評論公司的助理，你的任務是根據網路上的資料，來判斷其中有哪些店家要交給美食評論家去光顧，回答的規則如下"},
                {"role": "assistant", "content": "1. 所有的餐廳名稱須依順序加上編號，範例: 1. 餐廳名稱\n 2. 餐廳名稱"},
                {"role": "assistant", "content": "2. 所列出的餐廳名稱必須出現在交給您的網路搜尋的結果裡"},
                {"role": "assistant", "content": f"3. 餐廳的數量上限為{min(10,needed)}間 "},
                {"role": "assistant", "content": f"4. 請提供{needed}間餐廳 "},
                {"role": "assistant", "content": "5. 除非提供的資料內有規則1列出的餐廳，才可列入清單"},
                {"role": "assistant", "content": "以下為範例，包含3個搜尋結果跟回答"},
                {"role": "assistant", "content": "1. 說到道地的美食就不得不提到阿財羊肉爐......"},
                {"role": "assistant", "content": "2. 道地美食No.1 好喝豆漿 No.2 洪記牛肉麵....."},
                {"role": "assistant", "content": "3. 聽說凱霞牛肉湯十分有名......"},
                {"role": "assistant", "content": "Ans:"},
                {"role": "assistant", "content": "1. 阿財羊肉爐"},
                {"role": "assistant", "content": "2. 好喝豆漿"},
                {"role": "assistant", "content": "3. 洪記牛肉麵"},
                {"role": "assistant", "content": "4. 凱霞牛肉湯"},
                {"role": "assistant", "content": "以下為另一個範例，包含3個搜尋結果跟回答"},
                {"role": "assistant", "content": "1. 咖哩的食材包括胡蘿蔔......"},
                {"role": "assistant", "content": "2. 烤箱先加熱10分鐘....."},
                {"role": "assistant", "content": "3. 食材推薦去全聯買......"},
                {"role": "assistant", "content": "Ans:"},
                {"role": "assistant", "content": "搜尋結果裡沒有包含任何餐廳"},
                {"role": "assistant", "content": f"\n 接下來我會給你{perExtract}份搜尋結果"},
                {"role": "assistant", "content": f"請依照接下來提供的結果依據規則提取出餐廳名單"},
                {"role": "assistant", "content": f"搜尋結果:"}
            ]
            for i in range(startPoint,min(startPoint+perExtract,len(searchResult))) :
                sendMessage.append({"role": "assistant", "content": f"{i+1}. " + searchResult[i]})

            return sendMessage

                  
    def restaurantGenerate(self, place, mode, needed, searchResult = [], startPoint = 0, perExtract = 0):
        if mode == 0:
            print("-----------------Generate Restaurant List Random by GPT-----------------")
        else:
            print("-----------------Generate Restaurant List by GPT-----------------")
        openai.api_key = self.OPENAIAPI

        sendMessage = self.messageGenerate(place, mode, needed, searchResult, startPoint, perExtract)

        sendMessage.append({"role": "user", "content": "Ans:"})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=sendMessage
        )


        if(self.defTest):
            print(f"MessageSend : {sendMessage}")
            print(f"Response : {response['choices'][0]['message']['content']}")
        
        return response['choices'][0]['message']['content']




