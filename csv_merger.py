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


file_pathA = './maybeNegativeOrNature_foodQualityA.csv'
file_pathB= './maybeNegativeOrNature_foodQualityB.csv'
output_file_path = './maybeNegativeOrNature_foodQualityMerge.csv'



# 呼叫函式來讀取CSV檔案
csv_dataA = read_csv_file(file_pathA)
csv_dataB = read_csv_file(file_pathB)
csv_dataMerge = read_csv_file(file_pathA)

columns = csv_dataA.columns
MERGESIZE = min(11000,len(csv_dataA.index))
chk = int(MERGESIZE / 100)
step = 0

deafult = np.zeros((1,len(csv_dataA.iloc[0][3:].values)), dtype='O')[0]

#test = np.array(csv_dataA.iloc[100000][3:].values)
#print(np.array_equal(test, deafult))
for i in csv_dataA.index:
    #print(i)
    if (i+1) % chk == 0:
        step += 1
        print(f"{step}%")

    test = csv_dataA.iloc[i][3:].values
    if i > MERGESIZE:
        break
    if np.array_equal(test, deafult) == False:
        csv_dataMerge.iloc[i] = csv_dataA.iloc[i]
    else:
        csv_dataMerge.iloc[i] = csv_dataB.iloc[i]

write_to_csv(csv_dataMerge, output_file_path)