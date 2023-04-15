"""
Nonblocking IO

error.EAGAIN

短写: send 函数丢弃了剩余的字节


Created at 2023/4/15
"""
import errno
import socket


def func():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('localhost', 0))
    listener.listen(1)

    client = socket.create_connection(listener.getsockname())
    server, addr = listener.accept()

    client.setblocking(False)

    try:
        while True:
            client.sendall(b'*' * 1024)
    except socket.error as e:
        print(e.errno == errno.EAGAIN)


def func_send():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('localhost', 0))
    listener.listen(1)

    client = socket.create_connection(listener.getsockname())
    server, addr = listener.accept()

    server.setblocking(False)

    try:
        while True:
            print(server.send(b'*' * 1024))
    except socket.error as e:
        print('terminated with e: {}'.format(e.errno))


if __name__ == '__main__':
    func_send()
