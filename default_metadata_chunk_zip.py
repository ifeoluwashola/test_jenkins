import glob
import zipfile
from zipfile import ZipFile, ZIP_DEFLATED
import os
import json
import shutil


def create_metadata(baseDir):
    files = glob.glob(f'{baseDir}/*/')
    for folderpath in files:
        with open(folderpath + "/metadata.json", "w") as f:
            data = {
                "collectorless_connector_name": "legacy",
                "collectorless_connector_version": "0.0.0",
                "nms_version": "0.0.0"
            }
            res = json.dumps(data)
            f.write(res)


def zipdir(baseDir):
    files = glob.glob(f'{baseDir}/*/')
    for folder in files:
        ziph = ZipFile( f'./zip_output/{folder.split("/")[2]}.zip', 'w', ZIP_DEFLATED)
        # path= './output'
        length = len(folder)
        # ziph is zipfile handle
        for root, dirs, files in os.walk(folder):
            folder = root[length:]
            for file in files:
                if file.startswith('config'):
                    filename="show_running-config"    # to get flatfile
                    ziph.write(os.path.join(root, file), os.path.join(folder, filename))
                elif file.startswith('inventory'):
                    filename="MIBS"    # to get flatfile
                    ziph.write(os.path.join(root, file), os.path.join(folder, filename))
                else:
                    ziph.write(os.path.join(root, file), os.path.join(folder, file))
            for dir in dirs:
                ziph.write(os.path.join(root, dir), os.path.join(folder, dir))
        ziph.close()


def delete_all(baseDir):
    folder = glob.glob(f'{baseDir}/*.zip')
    for filename in folder:
        try:
            if os.path.isdir(filename):
                shutil.rmtree(filename)
            elif os.path.isfile(filename) or os.path.islink(filename):
                os.unlink(filename)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (filename, e))

# zipdir('./output')