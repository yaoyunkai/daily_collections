"""


Created at 2023/4/19
"""
import paramiko


class Shell(object):
    def __init__(self, host, username, password, timeout=90):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=host, username=username, password=password)

        self.__chan: paramiko.Channel = ssh_client.invoke_shell()
        self.__chan.settimeout(timeout)
