"""
Windows Management Instrumentation (WMI) API

Created at 2023/3/7
"""

import wmi

# create a WMI object
wmi_obj = wmi.WMI()

# get all the processes running on the system
processes = wmi_obj.Win32_Process()

print(len(processes))

# loop through each process and get its TCP connections
for idx, process in enumerate(processes):
    if idx == 234:
        connections = wmi_obj.query("SELECT * FROM Win32_PerfRawData_Tcpip_TCPv4 WHERE OwningProcess={}".format(process.ProcessId))

        # print out the process name and its TCP connections
        print("Process Name: {}".format(process.Name))
        for connection in connections:
            print("    Connection: {}:{} -> {}:{} ({})".format(connection.IPv4LocalAddress, connection.IPv4LocalPort, connection.IPv4RemoteAddress, connection.IPv4RemotePort, connection.State))
