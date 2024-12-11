"""


Created at 2023/4/6
"""
import socket
import time


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 45000))

    count = 1
    msg = 'hello world, %s'
    sock.sendall((msg % count).encode('utf8'))

    while True:
        data = sock.recv(1024)
        print('recv data from server: ', data)
        count += 1
        sock.sendall((msg % count).encode('utf8'))
        time.sleep(3)


if __name__ == '__main__':
    run()
