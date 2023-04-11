"""


Created at 2023/4/10

"""

import socket
import time


def create_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect(('10.79.176.187', 9000))
    sock.connect(('localhost', 9000))

    print(sock.getpeername())  # get remote address
    print(sock.getsockname())  # get local address

    # sock.sendall(b'1234567')
    # sock.sendall(b'3333333333')
    sock.sendall(b'23456')

    try:
        while True:
            data = sock.recv(1024)
            if data:
                print('recv from server:', data)
            sock.sendall(data)
            time.sleep(3)
    except KeyboardInterrupt:
        sock.close()


if __name__ == '__main__':
    create_client()
