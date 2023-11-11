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

def write_to_csv(df, file_path, errCount = 0):
    try:
        df.to_csv(file_path, index=False)
        return False
    except:
        if errCount > 3:
            return True
        else:
            errCount += 1
            write_to_csv(df, file_path, errCount)

def read_csv_file(file_path):
    data = pd.read_csv(file_path)
    return data

def enter_help(csvsaveErr):
    print('Enter Type:')
    for key, value in typeDic.items():
        print(f"{key}: {value}", end=" | ")
    print(f"q: quit, a: add new type, n: next row, r: remove type, c: clear all type, ni: NonImportant")
    if(csvsaveErr):
        print("/n THERE IS A CSV SAVE ERROR, PLEASE NOT CLOSE THE PROGRAM UNTIL NEXT WRITE")
    
pd.set_option('display.max_colwidth', None)

def refreshInfo(index,csvsaveErr):
    clear_console()
    print(f"data No.{index}")
    print(csv_data.loc[index])
    enter_help(csvsaveErr)


csvsaveErr = False
# 假設你的CSV檔案名稱為data.csv，並且與程式碼檔案位於同一個目錄下
file_path = './maybePositiveEnvironment.csv'
output_file_path = './maybePositiveEnvironment.csv'
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
        if row[i] != 0:
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
    while True:
        refreshInfo(index,csvsaveErr)
        inputType = input()
        
        if inputType == 'a':
            print("input new type, -999 to quit:")
            newType = input()
            if newType == '-999':
                continue
            typeDic[len(typeDic)] = newType
            csv_data[newType] = '0'
            csvsaveErr = write_to_csv(csv_data, output_file_path)
            
        elif inputType == 'q':
            quit = True
            break
        elif inputType == 'n':
            next = True
            break
        elif inputType == 'c':
            for key, value in typeDic.items():
                csv_data.loc[index, typeDic[key]] = 0
            csvsaveErr = write_to_csv(csv_data, output_file_path)
            continue
        elif inputType == "ni":
            for key, value in typeDic.items():
                csv_data.loc[index, typeDic[key]] = 0
            csv_data.loc[index, 'NonImportant'] = 1
            csvsaveErr = write_to_csv(csv_data, output_file_path)
            refreshInfo(index,csvsaveErr)
            continue
             
        elif inputType == 'r':
            while True:
                print("Enter Row to remove, -999 to quit:")
                for key, value in typeDic.items():
                    print(f"{key}: {value}", end=" | ")
                print()
                removeRow = None
                try:
                    removeRow = int(input())
                except:
                    print("Wrong input")
                    continue
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
                                csvsaveErr = write_to_csv(csv_data, output_file_path)
                                break
                        else:
                            break
                elif removeRow == -999:
                    break
                else:
                    print("Wrong input")
                    continue
            

        typeSelect = None
        try:
            typeSelect = int(inputType)
        except:
            print("Wrong input")
            continue

        if typeSelect in typeDic:
            while True:
                print("input Score(1-5) or notEdit(0)")
                inputScore = None
                try:
                    inputScore = int(input())
                except:
                    print("Wrong input")
                    continue
                if inputScore > 0 and inputScore <= 5:
                    csv_data.loc[index, typeDic[int(inputType)]] = inputScore
                    csvsaveErr = write_to_csv(csv_data, output_file_path)
                    break
                elif inputScore == 0:
                    csv_data.loc[index, typeDic[int(inputType)]] = 0
                    csvsaveErr = write_to_csv(csv_data, output_file_path)
                    break
                print("Wrong input")
        else:
            print("Wrong input")
            continue

        refreshInfo(index,csvsaveErr)

    if quit:
        break
    if next:
        continue
