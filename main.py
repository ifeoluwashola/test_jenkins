from Inventory_data import *
from config_data import *
from default_metadata_chunk_zip import *
from os.path import exists
from data_retrieval import *

# today=date.today()
today="2022-05-01"
baseDir='./Output'
n=5
chunksize=1


# download_zip_file(today)
if exists(f"./Input/{today}_inventory_test.csv") and exists(f"./Input/{today}_config_test.csv") and exists(f"./Input/{today}_SNMP"):
    exit()
if exists(f"./Input/{today}_inventory_test.csv") and exists(f"./Input/{today}_config_test.csv"):
    inventory_files_in_chunks(today, chunksize, n, baseDir)
    create_mib_from_inventory(baseDir)
    device_config_in_chunks(today,baseDir)
    create_metadata(baseDir)
    zipdir(baseDir)
    # upload()
elif exists(f"./Input/{today}_SNMP"):
    inventory_files_in_chunks_SNMP(chunksize, n, baseDir)
    create_metadata(baseDir)
    zipdir(baseDir)
#     # upload()
else:
    exit()

print("Data processing completed.")


