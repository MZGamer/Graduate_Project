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

file_pathA = './reviewTypeA.csv'
file_pathB= './reviewTypeB.csv'
output_file_path = './reviewTypeMerge.csv'
# 呼叫函式來讀取CSV檔案
csv_dataA = read_csv_file(file_pathA)
csv_dataB = read_csv_file(file_pathB)
csv_dataMerge = read_csv_file(file_pathA)

columns = csv_dataA.columns
print(csv_dataA.index)
chk = int(len(csv_dataA.index) / 100)
step = 0
for i in csv_dataA.index:
    print(i)
    if i+1 % chk == 0:
        step += 1
        print(f"{step}%")
    for r in (columns[3:]):
        if csv_dataA.iloc[i][r] == 1 or csv_dataA.iloc[i][r] == -1:
            csv_dataMerge.iloc[i] = csv_dataA.iloc[i]
            break
        elif csv_dataB.iloc[i][r] == 1 or csv_dataB.iloc[i][r] == -1:
            csv_dataMerge.iloc[i] = csv_dataB.iloc[i]
            break

write_to_csv(csv_dataMerge, output_file_path)