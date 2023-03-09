import os
from collections import OrderedDict
import json
import pandas as pd
import glob
import shutil
import pkg_resources
import re
import pprint
from SysDescTemplate import *
import logging

LOGGER = logging.getLogger(__name__ + ".acimib_builder")

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def inventory_files_in_chunks(today, chunksize, n, dirpath):
    dict1 = {}
    # data = pd.read_csv(f"./Input/Sample_inventory.csv")
    data = pd.read_csv(f"./Input/{today}_inventory_test.csv")
    row_value = data.DeviceName + ":" + data.ManagementIP
    for row in row_value:
        dict1[row.split(":")[0]] = row.split(":")[1]
    res1 = list(OrderedDict.fromkeys(data.DeviceName))
    l= list(divide_chunks(res1, n))
    for file in l:
        baseDir = os.path.join(dirpath, f'chunk_{chunksize}')
        if not os.path.exists(baseDir):
            os.makedirs(baseDir)
        for value in file:
            folderName = value
            UserPath = os.path.join(baseDir, folderName)
            if not os.path.exists(os.path.join(baseDir, folderName)):
                os.makedirs(UserPath)
            with open(UserPath + "/metadata.json", "w") as f:
                data1 = {
                    "IPAddress": dict1[value],  # Use ManagementIP
                    "PrimaryDeviceName": value,  # Use DeviceName
                }
                res = json.dumps(data1)
                f.write(res)
            value = data.groupby(data.DeviceName).get_group(value)
            value.to_csv(UserPath + "/MIBS", index=False)
        chunksize=chunksize+1
    return chunksize

def inventory_files_in_chunks_SNMP(chunksize, n, dirpath):
    SNMP_dir='./Input/2022-05-01_SNMP'
    value=[]
    for files in glob.glob(f'{SNMP_dir}/*'):
        file= files.split("/")[3].split(".")[0]
        value.append(file)
    l = list(divide_chunks(value, n))
    for file in l:
        baseDir = os.path.join(dirpath, f'chunk_{chunksize}')
        if not os.path.exists(baseDir):
            os.makedirs(baseDir)
        for value in file:
            IPAddress = ""
            folderName = value
            UserPath = os.path.join(baseDir, folderName)
            if not os.path.exists(os.path.join(baseDir, folderName)):
                os.makedirs(UserPath)
            shutil.move(f'{SNMP_dir}/{value}.log', f'{UserPath}/MIBS')
            with open(UserPath + "/MIBS", "r") as f1:
                for line in f1:
                    if ".1.3.6.1.2.1.4.20.1.1" in line:
                        IPAddress=line.split(":")[1].strip()
            with open(UserPath + "/metadata.json", "w") as f:
                data1 = {
                    "IPAddress": IPAddress,  # Use ManagementIP
                    "PrimaryDeviceName": value,  # Use DeviceName
                }
                res = json.dumps(data1)
                f.write(res)
        chunksize = chunksize + 1

def create_vendors_oid_tree_dict():
    filename = pkg_resources.resource_filename(__name__, "OIC_files/CISCO-ENTITY-VENDORTYPE-OID-MIB.my")

    oid_tree_dict_in = {"CISCOENTITYVENDORTYPEOIDMIB": {'parent_oid': False, 'oid_current': "1.3.6.1.4.1.9.12.3"},
                        "CISCOPRODUCTS": {'parent_oid': False, 'oid_current': "1.3.6.1.4.1.9.1"}}
    with open(filename, "r", encoding='utf8') as outfile:
        temp_data = outfile.readlines()
        for line in temp_data:
            oid_group = re.search(r'^(\S+)\s+OBJECT IDENTIFIER\s+::=\s+\{\s+(\S+)\s+(\S+)\s+\}(\s+--(.*?)\s*$){0,1}',
                                  line)
            if oid_group:
                oid_tree_dict_in[oid_group.group(1).upper()] = {'parent_oid': oid_group.group(2).upper(),
                                                                'oid_current': oid_group.group(3)}
    # TODO : fix var name reused
    filename = pkg_resources.resource_filename(__name__, "OIC_files/CISCO-PRODUCTS-MIB.my")

    with open(filename, "r", encoding='utf8') as outfile:
        temp_data = outfile.readlines()
        for line in temp_data:
            oid_group = re.search(r'^(\S+)\s+OBJECT IDENTIFIER\s+::=\s+\{\s+(\S+)\s+(\S+)\s+\}(\s+--(.*?)\s*$){0,1}',
                                  line)
            if oid_group:
                oid_tree_dict_in[oid_group.group(1).upper()] = {'parent_oid': oid_group.group(2).upper(),
                                                                'oid_current': oid_group.group(3)}

    return oid_tree_dict_in

def create_vendors_oid_tree_dict_sysobjectid():
    oid_tree_dict_in1 = {"CISCOENTITYVENDORTYPEOIDMIB": {'parent_oid': False, 'oid_current': "1.3.6.1.4.1.9.12.3"},
                        "CISCOPRODUCTS": {'parent_oid': False, 'oid_current': "1.3.6.1.4.1.9.1"}}
    filename = pkg_resources.resource_filename(__name__, "OIC_files/CISCO-PRODUCTS-MIB.my")

    with open(filename, "r", encoding='utf8') as outfile:
        temp_data = outfile.readlines()
        for line in temp_data:
            oid_group = re.search(r'^(\S+)\s+OBJECT IDENTIFIER\s+::=\s+\{\s+(\S+)\s+(\S+)\s+\}(\s+--(.*?)\s*$){0,1}',
                                  line)
            if oid_group:
                oid_tree_dict_in1[oid_group.group(1).upper()] = {'parent_oid': oid_group.group(2).upper(),
                                                                'oid_current': oid_group.group(3)}

    return oid_tree_dict_in1

def find_vendor_type_oid_sysobjectid(oid_tree_dict: dict, model_name: str) -> str:
    complete_oid=""
    model_name = model_name.replace('-', '')
    model_name = re.sub(r"/.*", "", model_name)
    for key in oid_tree_dict.keys():
        if re.search(model_name, key):
            print("Key for sysobjectid",key)
            complete_oid = oid_tree_dict[key]['oid_current']
            parent_oid = oid_tree_dict[key]['parent_oid']
            while parent_oid:
                complete_oid = oid_tree_dict[parent_oid]['oid_current'] + '.' + complete_oid
                parent_oid = oid_tree_dict[parent_oid]['parent_oid']

    return complete_oid

def find_vendor_type_oid(oid_tree_dict: dict, model_name: str) -> str:

    model_name=model_name.upper()
    complete_oid = oid_tree_dict[model_name]['oid_current']
    parent_oid = oid_tree_dict[model_name]['parent_oid']
    while parent_oid:
        complete_oid = oid_tree_dict[parent_oid]['oid_current'] + '.' + complete_oid
        parent_oid = oid_tree_dict[parent_oid]['parent_oid']

    return complete_oid

def ent_physical_vendor_type_chassis(oid_tree_dict, modelname):
    model_name = 'cevChassis' + modelname.replace('-', '')
    # print("model_name", model_name)
    if 'APIC' in model_name:
        physical_vendor_type = '1.3.6.1.4.1.9.1.2238'
    else:
        try:
            physical_vendor_type = find_vendor_type_oid(oid_tree_dict, model_name)
        except Exception as e:
            LOGGER.warning("Exception : {error} - no oid found for model name : {mn}".format(mn=model_name,
                                                                                             error=e))
            physical_vendor_type = "0.0.0"

    return physical_vendor_type

def ent_physical_vendor_type_container(modelname) -> str:
    if modelname == "eqptLCSlot":
        return ".1.3.6.1.4.1.9.12.3.1.5.123"
    elif modelname == "eqptSupCSlot" or modelname == "eqptSysCSlot" or modelname == "eqptFCSlot":
        return ".1.3.6.1.4.1.9.12.3.1.5.122"
    else:
        return ""

def ent_physical_vendor_type_module(oid_tree_dict, modelname) -> str:
    base_name = "cevModule"
    model_name = base_name + modelname.replace('-', '')
    # print("model_name", model_name)
    try:
        vendor_type = find_vendor_type_oid(oid_tree_dict, model_name)
    except KeyError:
        vendor_type = "0.0.0"
    if vendor_type=="0.0.0":
        new_model_name = "cev" + modelname.replace('-', '') + "FixedModule"
        print("new Model",new_model_name)
        try:
            vendor_type = find_vendor_type_oid(oid_tree_dict, new_model_name)
        except KeyError:
            LOGGER.warning("Exception : no oid found for Supervisor Card model name : {mn}".format(
                mn=model_name))
    return vendor_type

def ent_physical_vendor_type_fan(oid_tree_dict, modelname) -> str:
    base_name = "cevFan"
    model_name = base_name + modelname.replace('-', '')
    # print("model_name",model_name)
    try:
        vendor_type = find_vendor_type_oid(oid_tree_dict, model_name)
    except KeyError:
        vendor_type = "0.0.0"

    if not vendor_type:
        model_name = model_name + "Tray"
        try:
            vendor_type = find_vendor_type_oid(oid_tree_dict, model_name)
        except KeyError:
            LOGGER.warning("Exception : no oid found for Ft model name : {mn}".format(mn=model_name))
            vendor_type = "0.0.0"

    return vendor_type

def ent_physical_vendor_type_powerSupply(oid_tree_dict, modelname) -> str:
        base_name = "cevPowerSupply"
        model_name = base_name + modelname.replace('-', '')
        # print("model_name", model_name)
        try:
            vendor_type = find_vendor_type_oid(oid_tree_dict, model_name)
        except KeyError:
            LOGGER.warning("Exception : no oid found for Psu model name : {mn}".format(mn=model_name))
            vendor_type = "0.0.0"
        return vendor_type

POD_NODE_entPhysicalClass = {
    'LC': 9,  # Module
    'FC': 9,  # Module
    'SupC': 9,  # Module
    'SysC': 9,  # Module
    'RP': 9,  # Module
    'SC': 9,  # Module
    'module': 9,  # Module
    'Module': 9,  # Module
    'Slot': 9,  # Module
    'subslot': 9,  # Module
    'Chassis': 3,  # Chassis
    'CISCO': 3,  # Chassis
    'Rack': 3,  # Chassis
    'LCSlot': 5,  # Container
    'FCSlot': 5,  # Container
    'SupCSlot': 5,  # Container
    'SysCSlot': 5,  # Container
    'PsuSlot': 5,  # Container
    'FtSlot': 5,  # Container
    'PM': 6,  # powerSupply
    'PT': 6,  # powerSupply
    'Power': 6,  # powerSupply
    'Ft': 7,  # Fan
    'Fan': 7,  # Fan
    'CPU': 12,  # CPU
    'LeafP': 10,  # Port
    'SFP': 10,  # Port
    'Supervisor': 10,  # Port
    'FabP': 10,  # Port
    'GigabitEthernet': 10,  # Port
    'Sensor': 8  # Sensor
}

Module = ['LC','FC','SupC','RP','SC','module','Module','Slot', 'subslot', 'CPU']
Chassis = ['Chassis','CISCO','Rack']
Container = ['LCSlot','FCSlot','SupCSlot','SysCSlot','PsuSlot','FtSlot']
PowerSupply = ['PM','PT','Power']
Fan = ['Ft','Fan', 'FT']
# Cpu = ['CPU']
Port = ['LeafP','SFP','Supervisor','FabP','GigabitEthernet']
Sensor = ['Sensor']


def create_mib_from_inventory(dirpath):
    OID_tree = create_vendors_oid_tree_dict()
    print("OID tree created")
    for element in glob.iglob(dirpath + '/**/*.csv', recursive=True):
        if 'inventory' in element:
            data = pd.read_csv(element)
            new_file_content = ""
            devicename=list(set(data.DeviceName))[0]
            new_line1 = f'.1.3.6.1.2.1.1.5.0 = STRING: {devicename}'
            new_file_content += new_line1 + "\n"
            IpAddress = list(set(data.ManagementIP))[0]
            new_line2 = f'.1.3.6.1.2.1.4.20.1.1.{IpAddress} = IpAddress: {IpAddress}'
            new_file_content += new_line2 + "\n"
            print(devicename)
            chassis_index=data.Name[(data.Name == "Chassis") | (data.Name == "Rack 0") | (data.Name == "Supervisor(slot 1)")]
            if not chassis_index.empty:
                index_value = chassis_index.index[0]
            else:
                index_value= -1

            #Sysdescription
            PID=data.PId.iloc[index_value]
            Platform=data.HardwareSku.iloc[index_value]
            Version=data.OSVersion.iloc[index_value]
            print(PID, "___", Platform, "____", Version)
            if any(word in Platform for word in Nexus_device):
                new_line9 = f'.1.3.6.1.2.1.1.1.0 = STRING: {Nexus(PID, Version)}'
                new_file_content += new_line9 + "\n"
            elif any(word in Platform for word in IOS_device):
                new_line9 = f'.1.3.6.1.2.1.1.1.0 = STRING: {IOS(PID, Version)}'
                new_file_content += new_line9 + "\n"
            elif any(word in Platform for word in IOS_XR_device):
                new_line9 = f'.1.3.6.1.2.1.1.1.0 = STRING: {IOS_XR(PID, Version)}'
                new_file_content += new_line9 + "\n"
            else:
                new_line9 = f'.1.3.6.1.2.1.1.1.0 = STRING: Cisco Device'
                new_file_content += new_line9 + "\n"

            #sysobjectid
            OID_tree1 = create_vendors_oid_tree_dict_sysobjectid()
            oid = find_vendor_type_oid_sysobjectid(OID_tree1, data.PId.iloc[index_value])
            print("find OID relevant to PID")
            if oid:
                new_line8 = f'.1.3.6.1.2.1.1.2.0 = OID: .{oid}'
                new_file_content += new_line8 + "\n"
            else:
                value=ent_physical_vendor_type_chassis(OID_tree, data.PId.iloc[index_value])
                new_line8 = f'.1.3.6.1.2.1.1.2.0 = OID: {value}'
                new_file_content += new_line8 + "\n"

            #physicalentity table
            for i, n in enumerate(data.PId):
                new_line3= f'.1.3.6.1.2.1.47.1.1.1.1.13.{i+1} = STRING: "{n}"'
                new_file_content += new_line3 + "\n"
            for j,m in enumerate(data.SerialNo):
                new_line4=f'.1.3.6.1.2.1.47.1.1.1.1.11.{j+1} = STRING: "{m}"'
                new_file_content += new_line4 + "\n"
            for k,l in enumerate(data.OSVersion):
                new_line5=f'.1.3.6.1.2.1.47.1.1.1.1.10.{k+1} = STRING: "{l}"'
                new_file_content += new_line5 + "\n"
            for x,y in enumerate(data.Description):
                new_line6=f'.1.3.6.1.2.1.47.1.1.1.1.2.{x+1} = STRING: "{y}"'
                new_file_content += new_line6 + "\n"
            for o,p in enumerate(data.VId):
                new_line7=f'.1.3.6.1.2.1.47.1.1.1.1.8.{o+1} = STRING: "{p}"'
                new_file_content += new_line7 + "\n"

            #Physical class
            for a,b in enumerate(data.Name):
                for key, value in POD_NODE_entPhysicalClass.items():
                     if (key in b):
                        new_file_content += f'.1.3.6.1.2.1.47.1.1.1.1.5.{a+1} = INTEGER: {value}' + "\n"
                        break
                if re.match('0\/\d+$',b):
                    new_file_content += f'.1.3.6.1.2.1.47.1.1.1.1.5.{a + 1} = INTEGER: 9' + "\n"

            #Physical containID
            for c, d in enumerate(data.Name):
                if index_value == c:
                    new_file_content += f'.1.3.6.1.2.1.47.1.1.1.1.4.{c + 1} = INTEGER: 0' + "\n"
                else:
                    new_file_content += f'.1.3.6.1.2.1.47.1.1.1.1.4.{c + 1} = INTEGER: {index_value+1}' + "\n"

            #physical vendor type
            for e, f in enumerate(data.Name):
                # print("vendorOID element", e, f)
                if any(word in f for word in Fan):
                    vendor_type=ent_physical_vendor_type_fan(OID_tree,data.PId.iloc[e])
                    new_file_content += f'.1.3.6.1.2.1.47.1.1.1.1.3.{e + 1} = OID: .{vendor_type}' + "\n"
                elif any(word in f for word in PowerSupply):
                    vendor_type = ent_physical_vendor_type_powerSupply(OID_tree, data.PId.iloc[e])
                    new_file_content += f'.1.3.6.1.2.1.47.1.1.1.1.3.{e + 1} = OID: .{vendor_type}' + "\n"
                elif any(word in f for word in Module):
                    vendor_type = ent_physical_vendor_type_module(OID_tree, data.PId.iloc[e])
                    new_file_content += f'.1.3.6.1.2.1.47.1.1.1.1.3.{e + 1} = OID: .{vendor_type}' + "\n"
                elif any(word in f for word in Chassis):
                    vendor_type = ent_physical_vendor_type_chassis(OID_tree, data.PId.iloc[e])
                    new_file_content += f'.1.3.6.1.2.1.47.1.1.1.1.3.{e + 1} = OID: .{vendor_type}' + "\n"
                else:
                    new_file_content += f'.1.3.6.1.2.1.47.1.1.1.1.3.{e + 1} = OID: .0.0.0' + "\n"

            writing_file = open(element, "w")
            writing_file.write(new_file_content)
            writing_file.close()


