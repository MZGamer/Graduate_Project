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


file_pathA = './maybePortion.csv'
file_pathB= './reviewDatasetV5.csv'
output_file_path = './reviewDatasetV6.csv'



# 呼叫函式來讀取CSV檔案
csv_dataA = read_csv_file(file_pathA)
csv_dataB = read_csv_file(file_pathB)

columns = csv_dataA.columns

res = pd.concat([csv_dataB,csv_dataA],axis=0, ignore_index=True)
res.drop_duplicates(subset=['Comment'], keep='last', inplace=True)

write_to_csv(res, output_file_path)