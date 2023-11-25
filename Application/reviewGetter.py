from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
import csv
from selenium.webdriver.common.action_chains import ActionChains
from restaurant import Restaurant
import os


def getReview(DBBuildingList, defTest = False):

    restaurant_list = DBBuildingList
    finishedList = []
    driver = webdriver.Chrome()
    driver.set_window_size(850,750)
    Map_coordinates = dict({
        "latitude": 22.6,
        "longitude": 120.3,
        "accuracy": 100
        })
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", Map_coordinates)
    #London Victoria & Albert Museum URL
    url = "https://www.google.com.tw/maps/@22.6612676,120.3031559,17z?hl=zh-TW"
    driver.get(url)
    time.sleep(3)
    counter = 0
    for index in range(len(restaurant_list)):
        if(defTest):
            print(f"{index} / {len(restaurant_list)} {restaurant_list[index].name}")
        restaurant = restaurant_list[index]
        url = f"https://www.google.com/maps/search/?api=1&query={restaurant.location}&query_place_id={restaurant.placeID}"
        driver.get(url)
        time.sleep(3)
        driver.find_element(By.XPATH, '//*[@class="hh2c6 "]').click()
        time.sleep(3)
        sortbutton = driver.find_elements(By.XPATH, '//*[@class="g88MCb S9kvJb "]')
        try:
            sortbutton[2].click()
        except:
            if(defTest):
                print("maybe not restaurant")
                print(f"{i} : {restaurant.name}")
            continue
        time.sleep(1)
        sortselect = driver.find_elements(By.XPATH, '//*[@class="fxNQSd"]')
        try:
            sortselect[1].click()
        except:
            if(defTest):
                print("maybe not restaurant")
                print(f"{i} : {restaurant.name}")
            continue
        
        time.sleep(1)
        scrollable_div = driver.find_element(By.XPATH, '//*[@class="m6QErb DxyBCb kA9KIf dS8AEf "]')
        for i in range(0,min(round(int(restaurant.raitingTotal) / 10),65)):#867/10 - 1
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
            time.sleep(0.5)
        buttons = driver.find_elements(By.XPATH, '//*[@class="w8nwRe kyuRq"]')
        for button in buttons:
            button.click()
            time.sleep(0.05)

        commendsFiled = driver.find_elements(By.XPATH, '//*[@class="jJc9Ad "]')

        s = ""
        repeatcontentBuffer = []
        for i in range(len(commendsFiled)):
            date = commendsFiled[i].find_element(By.CLASS_NAME, 'rsqaWe').text
            try:
                content = commendsFiled[i].find_element(By.CLASS_NAME, 'wiI7pd').text
            except:
                #print("no content")
                #print(commendsFiled[i].text.split("\n"))
                continue
            if(content in repeatcontentBuffer):
                continue
            else:
                repeatcontentBuffer.append(content)
                s = s + (date + "^" + content + "|")
        if (s == ""):
            continue
        restaurant_list[index].review = s
        finishedList.append(restaurant_list[index])
    return finishedList