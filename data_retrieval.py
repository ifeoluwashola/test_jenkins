import requests
import zipfile
import os
from zipfile import ZipFile, ZIP_DEFLATED


def download_zip_file(today):
    files=[f'{today}_inventory.zip', f'{today}_config.zip', f'{today}_SNMP.zip']
    for file in files:
        try:
            url = f'https://safecisco.blob.core.windows.net/inventory/{file}'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
            myfile = requests.get(url,headers=headers)
            open(f'./{file}', 'wb').write(myfile.content)
            with zipfile.ZipFile(f'./{file}', 'r') as zip_ref:
                zip_ref.extractall(f'./Input/')
            print(f'input_data folder has file for the date: {file.split(".")[0]}')
        except zipfile.BadZipfile:
            print(f'No {file.split("_")[1]} for date {today}')

    dir_name = "./"
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".zip"):
            os.remove(os.path.join(dir_name, item))