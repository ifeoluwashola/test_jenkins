import glob
import pandas as pd
import os
import csv


def device_config_in_chunks(today, baseDir):
    data = pd.read_csv(f"./Input/{today}_config_test.csv", header=None)
    # data = pd.read_csv(f"./Input/config_multiprocess.csv", header=None)
    list1=[]
    row_value = data.iloc[:, 0]
    files = glob.glob(f'{baseDir}/*/*/')
    s = {}
    for file in files:
        s[file.split('/')[3]] = file
    for value in row_value:
        folderName = value
        if folderName in s:
            UserPath = s[folderName]
            print("\nFolder exist for already present: ", UserPath)
            value = data.groupby(row_value).get_group(value)
            value1 = value.iloc[:, 1].str.replace(r'%%+', '\n', regex=True)
            value1.to_csv(UserPath + "/show_running-config", index=False, header=None, quoting=csv.QUOTE_NONE,
                          escapechar='\x1f')
        else:
            list1.append(folderName)
    return list1

