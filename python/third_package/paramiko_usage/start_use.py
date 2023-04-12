"""
export PS1="@\h DISCONNECTED-XXXXXX > "

Created at 2023/4/12
"""

import paramiko


def do_connect():
    # 设置SSH连接的参数
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('xxxx', username='xxxxxx', password='xxxxxxxxxxxx----')

    # 发送指令
    stdin, stdout, stderr = ssh.exec_command('ls -la')

    # 打印输出
    for line in stdout.readlines():
        print(line.strip())

    # 关闭连接
    ssh.close()


if __name__ == '__main__':
    do_connect()
