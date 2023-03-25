"""
use the Windows Performance Counters API

Created at 2023/3/7
"""
import psutil

# get the process ID of the target process
pid = 7832

# get the process object
process = psutil.Process(pid)

# loop through each connection and print its information
for connection in process.connections(kind='tcp'):
    print("Local Address: {}:{}".format(connection.laddr.ip, connection.laddr.port))
    print("Remote Address: {}".format(connection.raddr))
    print("Status: {}".format(connection.status))
