import csv
import pandas as pd
import os
import numpy as np

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


file_path= './reviewType_Empty2wTo4wV6.csv'
output_file_path = './reviewType_Empty2wTo4wV6.csv'
DETECTEMPTY = False

# 呼叫函式來讀取CSV檔案
csv_data = read_csv_file(file_path)

CLEANSIZE = min(1100000000,len(csv_data.index))
deafult = np.zeros((1,len(csv_data.iloc[0][3:].values)), dtype='O')[0]

columns = csv_data.columns
csv_data.drop(csv_data.index[CLEANSIZE+1:], inplace=True)

all = len(csv_data.index)
counter = 0
droplist = []
for index, row in csv_data.iloc[0:].iterrows():
    print(f"{all} / {counter}")
    counter += 1
    flag = False
    if(row["NonImportant"] != 0):
        droplist.append(index)
        continue
    test = csv_data.iloc[index][3:].values
    if np.array_equal(test, deafult) == DETECTEMPTY:
        droplist.append(index)
        continue

csv_data.drop(droplist, inplace=True)

write_to_csv(csv_data, output_file_path)