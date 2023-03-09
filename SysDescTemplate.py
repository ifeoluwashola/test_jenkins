Nexus_device=['Nexus']
IOS_device=['ASR', 'ISR', '2921']
IOS_XR_device=['88','NCS']


def Nexus(PID, Version):
    return "Cisco NX-OS(tm) {PID}, Software (NXOS 32-bit), Version {Version}, RELEASE SOFTWARE Copyright (c) 2002-2022 by Cisco Systems, Inc.".format(
        PID=PID,
        Version=Version
    )

def IOS(PID, Version):
    return "Cisco IOS Software, {PID} Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version {Version}, RELEASE SOFTWARE (fc3) Technical Support: http://www.cisco.com/techsupport Copyright (c) 1986-2021 by Cisco Systems, Inc.".format(
        PID=PID,
        Version=Version
    )

def IOS_XR(PID, Version):
    return "Cisco IOS XR Software ({PID}), Version {Version} Copyright (c) 2013-2019 by Cisco Systems, Inc.".format(
        PID=PID,
        Version=Version
    )

