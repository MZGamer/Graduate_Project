from time import sleep
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
    def messageGenerate(self, place, mode, needed, searchResult = [], startPoint = 0, perExtract = 0, restaurant : Restaurant = None, reviewList = []):
        if mode == 0:
            sendMessage =[
                {"role": "system", "content": "你是一個美食評論公司的助理，你的任務是根據你的記憶，來提供要交給美食評論家去光顧的店家，回答的規則如下"},
                {"role": "user", "content": "1. 所有的餐廳名稱須依順序加上編號，範例: 1. 餐廳名稱\n 2. 餐廳名稱"},
                {"role": "user", "content": f"2. 餐廳的數量上限為{min(10,needed)}間 "},
                {"role": "user", "content": f"3. 請提供{needed}間餐廳 "},
                {"role": "user", "content": "以下為範例"},
                {"role": "user", "content": "Q: 安南市"},
                {"role": "user", "content": "Ans:"},
                {"role": "user", "content": "1. 阿財羊肉爐"},
                {"role": "user", "content": "2. 好喝豆漿"},
                {"role": "user", "content": "3. 洪記牛肉麵"},
                {"role": "user", "content": "4. 凱霞牛肉湯"},
                {"role": "user", "content": f"\n 接下來我會給你地點"},
                {"role": "user", "content": f"請依照你的記憶提供餐廳名單"},
                {"role": "user", "content": f"Q:台灣{place}"}
            ]
            return sendMessage
        elif  mode == 1:
            sendMessage =[
                {"role": "system", "content": "你是一個美食評論公司的助理，你的任務是根據網路上的資料，來判斷其中有哪些店家要交給美食評論家去光顧，回答的規則如下\n "},
                {"role": "user", "content": "1. 所有的餐廳名稱須依順序加上編號，範例: 1. 餐廳名稱\n 2. 餐廳名稱\n "},
                {"role": "user", "content": "2. 所列出的餐廳名稱必須出現在交給您的網路搜尋的結果裡\n "},
                {"role": "user", "content": f"3. 餐廳的數量上限為{min(10,needed)}間 \n "},
                {"role": "user", "content": f"4. 請提供{needed}間餐廳 \n "},
                {"role": "user", "content": "5. 除非提供的資料內有規則1列出的餐廳，才可列入清單\n "},
                {"role": "user", "content": "以下為範例，包含3個搜尋結果跟回答\n "},
                {"role": "user", "content": "1. 說到道地的美食就不得不提到阿財羊肉爐......\n "},
                {"role": "user", "content": "2. 道地美食No.1 好喝豆漿 No.2 洪記牛肉麵.....\n "},
                {"role": "user", "content": "3. 聽說凱霞牛肉湯十分有名......\n "},
                {"role": "user", "content": "Ans:\n "},
                {"role": "user", "content": "1. 阿財羊肉爐\n "},
                {"role": "user", "content": "2. 好喝豆漿\n "},
                {"role": "user", "content": "3. 洪記牛肉麵\n "},
                {"role": "user", "content": "4. 凱霞牛肉湯\n "},
                {"role": "user", "content": "以下為另一個範例，包含3個搜尋結果跟回答\n "},
                {"role": "user", "content": "1. 咖哩的食材包括胡蘿蔔......\n "},
                {"role": "user", "content": "2. 烤箱先加熱10分鐘.....\n "},
                {"role": "user", "content": "3. 食材推薦去全聯買......\n "},
                {"role": "user", "content": "Ans:\n "},
                {"role": "user", "content": "搜尋結果裡沒有包含任何餐廳\n "},
                {"role": "user", "content": "以下為第三個範例，包含3個搜尋結果跟回答\n "},
                {"role": "user", "content": "1. 牛肉湯使用日本和牛......\n "},
                {"role": "user", "content": "2. 最好吃的壽司要用生魚.....\n "},
                {"role": "user", "content": "3. 愛河菜市場的魚最新鮮......\n "},
                {"role": "user", "content": "Ans\n :"},
                {"role": "user", "content": "搜尋結果裡沒有包含任何餐廳"},
                {"role": "user", "content": f"\n 接下來我會給你{perExtract}份搜尋結果\n "},
                {"role": "user", "content": f"請依照接下來提供的結果依據規則提取出餐廳名單\n "},
                {"role": "user", "content": f"搜尋結果:\n "}
            ]
            for i in range(startPoint,min(startPoint+perExtract,len(searchResult))) :
                sendMessage.append({"role": "user", "content": f"{i+1}. {searchResult[i]}\n "})

            return sendMessage
        else:
            sendMessage =[
                            {"role": "system", "content": "請以精選評論為主，餐廳評分為輔，以條列式分別列出這間餐廳的優點與缺點，並在最後做個總結。"},
                            {"role": "user", "content": "如有矛盾請指出並參考餐廳評分選擇列在優點或缺點"},
                            {"role": "user", "content": "請用繁體中文回答\n"},
                            {"role": "user", "content": "餐廳評分:"},
                            {"role": "user", "content": f"份量: {restaurant.detailRating[0]}/5"},
                            {"role": "user", "content": f"服務: {restaurant.detailRating[1]}/5"},
                            {"role": "user", "content": f"環境: {restaurant.detailRating[2]}/5"},
                            {"role": "user", "content": f"價格: {restaurant.detailRating[3]}/5"},
                            {"role": "user", "content": f"食物品質: {restaurant.detailRating[4]}/5\n"},
                            {"role": "user", "content": "精選評論:"},
                        ]
            for str in reviewList :
                sendMessage.append({"role": "user", "content": str})

            return sendMessage

                  
    def sendGPTRequest(self, place, mode, needed, searchResult = [], startPoint = 0, perExtract = 0, restaurant : Restaurant = None, reviewList = []):
        if mode == 0:
            print("-----------------Generate Restaurant List Random by GPT-----------------")
        elif mode == 1:
            print("-----------------Generate Restaurant List by GPT-----------------")
        else:
            print("-----------------Generate Restaurant Review by GPT-----------------")
        openai.api_key = self.OPENAIAPI

        sendMessage = self.messageGenerate(place, mode, needed, searchResult, startPoint, perExtract, restaurant, reviewList)

        sendMessage.append({"role": "user", "content": "Ans:"})
        
        if (mode != 2):
            modelSelect = "gpt-3.5-turbo-1106"
        else:
            modelSelect = "gpt-3.5-turbo-1106"

        try:
            response = openai.ChatCompletion.create(
                model=modelSelect,
                messages=sendMessage
            )
        except openai.error.RateLimitError:
            print("RateLimitWaiting")
            sleep(20)
            print("Retry")
            r = self.sendGPTRequest(place, mode, needed, searchResult, startPoint, perExtract, restaurant, reviewList)
            return r

        if(self.defTest):
            print(f"MessageSend : {sendMessage}")
            print(f"Response : {response['choices'][0]['message']['content']}")
        
        return response['choices'][0]['message']['content']




