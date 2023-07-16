import csv
import pandas as pd
import os

def from_x_to_x(numbers):
    result = []
    start = None
    end = None

    for num in numbers:
        if start is None:
            start = num
            end = num
        elif num == end + 1:
            end = num
        else:
            result.append((start, end))
            start = num
            end = num

    # 將最後一個區間加入結果
    if start is not None:
        result.append((start, end))

    # 格式化輸出
    output = ' '.join(f'{start} to {end}' if start != end else str(start) for start, end in result)

    # 輸出結果
    print(output)
def clear_console():
    # 檢查作業系統，並執行特定的清空螢幕指令
    os.system('cls' if os.name == 'nt' else 'clear')

def write_to_csv(df, file_path):
    df.to_csv(file_path, index=False)

def read_csv_file(file_path):
    data = pd.read_csv(file_path)
    return data

def enter_help():
    print('Enter Type:')
    for key, value in typeDic.items():
        print(f"{key}: {value}", end=" | ")
    print(f"q: quit, a: add new type, n: next row, r: remove type")
    
pd.set_option('display.max_colwidth', None)

# 假設你的CSV檔案名稱為data.csv，並且與程式碼檔案位於同一個目錄下
file_path = 'reviewType.csv'
output_file_path = 'reviewType.csv'
# 呼叫函式來讀取CSV檔案
csv_data = read_csv_file(file_path)

locmax = csv_data.shape[0] -1
columns = csv_data.columns
typeDic = {}
dicIndex = 0
for i in (columns[4:]):
    typeDic[dicIndex] = i
    dicIndex += 1

typeDic[-1] = 'NonImportant'
done = []
for index, row in csv_data.iloc[0:].iterrows():
    for i in (columns[3:]):
        if row[i] == 1 or row[i] == -1:
            done.append(index)
            break
print("following data is completed:")
from_x_to_x(done)



print(f'row is 0 to {locmax}')
print('Enter StartRow:')
start_row = 0

while True:
    start_row = int(input())
    if start_row > locmax or start_row < 0:
        print('StartRow Err, Enter StartRow:')
        continue
    break


# 輸出資料
for index, row in csv_data.iloc[start_row:].iterrows():
    quit = False
    next = False
    #print row
    clear_console()
    print("\n")
    print(f"data No.{index}")
    print(csv_data.loc[index])
    enter_help()
    while True:
        inputType = input()
        
        if inputType == 'a':
            print("input new type, -999 to quit:")
            newType = input()
            if newType == '-999':
                continue
            typeDic[len(typeDic)] = newType
            csv_data[newType] = '0'
            write_to_csv(csv_data, output_file_path)
            
        elif inputType == 'q':
            quit = True
            break
        elif inputType == 'n':
            next = True
            break
        elif inputType == 'r':
            while True:
                print("Enter Row to remove, -999 to quit:")
                for key, value in typeDic.items():
                    print(f"{key}: {value}", end=" | ")
                print()
                removeRow = int(input())
                if(removeRow == -1):
                    print("Can't remove NonImportant")
                    continue
                if removeRow in typeDic:
                    rmchk = 0
                    while True:
                        print(f"Are you sure to remove {typeDic[removeRow]}? y/n")
                        if input() == 'y':
                            if(rmchk < 3):
                                rmchk += 1
                            else:
                                csv_data = csv_data.drop(columns=[typeDic[removeRow]])
                                del typeDic[removeRow]
                                write_to_csv(csv_data, output_file_path)
                                break
                        else:
                            break
                elif removeRow == -999:
                    break
                else:
                    print("Wrong input")
                    continue
            

        
        elif int(inputType) in typeDic:
            while True:
                print("inputPositive(1) or Negative(-1) or notEdit(0)")
                inputPositive = int(input())
                if inputPositive == 1 or inputPositive == -1:
                    csv_data.loc[index, typeDic[int(inputType)]] = inputPositive
                    write_to_csv(csv_data, output_file_path)
                    break
                elif inputPositive == 0:
                    break
                print("Wrong input")
        else:
            print("Wrong input")
            continue

        clear_console()
        print(f"data No.{index}")
        print(csv_data.loc[index])
        enter_help()

    if quit:
        break
    if next:
        continue
