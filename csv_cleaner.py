import csv
import pandas as pd
import os

def write_to_csv(df, file_path, errCount = 0):
    try:
        df.to_csv(file_path, index=False)
    except:
        if errCount > 3:
            print("write to csv failed")
            raise Exception("write to csv failed")
        else:
            errCount += 1
            write_to_csv(df, file_path, errCount)

def read_csv_file(file_path):
    data = pd.read_csv(file_path)
    return data

file_path= './reviewType.csv'
output_file_path = './reviewTypeClean.csv'
# 呼叫函式來讀取CSV檔案
csv_data = read_csv_file(file_path)

columns = csv_data.columns
csv_data.drop(csv_data.index[3000:], inplace=True)

all = len(csv_data.index)
counter = 0
droplist = []
for index, row in csv_data.iloc[0:].iterrows():
    print(f"{all} / {counter}")
    counter += 1
    flag = False
    if(row["NonImportant"] == 1):
        droplist.append(index)
        continue
    for i in (columns[4:]):
        if row[i] == 1 or row[i] == -1:
            flag = True
            break
    if flag == False:
        droplist.append(index)
        continue

csv_data.drop(droplist, inplace=True)

write_to_csv(csv_data, output_file_path)