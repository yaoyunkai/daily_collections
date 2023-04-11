"""


Created at 2023/4/10
"""
import socket
import threading
import time


def do_func(sock, ):
    # print('----    start -------------')
    data = sock.recv(1024)
    if data:
        time.sleep(1)
        sock.sendall(b'FFF ' + data)
        sock.close()


def create_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 9000))
    sock.listen(2)

    while True:
        client_sock, addr = sock.accept()
        print('get conn:', addr)
        # time.sleep(0.6)
        # client_sock.sendall('123456789')
        # print('----------------------------------')

        threading.Thread(target=do_func, args=(client_sock,)).start()


if __name__ == '__main__':
    create_server()
