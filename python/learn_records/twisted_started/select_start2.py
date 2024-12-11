"""
file: select_start2.py
Created by Libyao at 2023/4/13


"""
import socket

import select


def select_start():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('localhost', 0))
    listener.listen(1)

    client = socket.create_connection(listener.getsockname())
    server, addr = listener.accept()

    maybe_readable = [listener, client, server]
    maybe_writeable = [client, server]

    can_read, can_write, _ = select.select(maybe_readable, maybe_writeable, [], 0)
    print(can_read)
    print(can_write)
    print('---------------------------')

    client.sendall(b'abc')
    can_read, can_write, _ = select.select(maybe_readable, maybe_writeable, [], 0)
    print(can_read)
    print(can_write)
    print('---------------------------')

    """
    只要数据保留在套接字的读缓冲区,它就会不断生成可读事件.
    写缓冲区有空间,就会一直生成写事件
    
    """
    can_read, can_write, _ = select.select(maybe_readable, maybe_writeable, [], 0)
    print(can_read)
    print(can_write)
    print('---------------------------')

    print(server.recv(1024) == b'abc')

    can_read, can_write, _ = select.select(maybe_readable, maybe_writeable, [], 0)
    print(can_read)
    print(can_write)
    print('---------------------------')


def test_client_close():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('localhost', 0))
    listener.listen(1)

    client = socket.create_connection(listener.getsockname())
    server, addr = listener.accept()

    maybe_readable = [listener, client, server]
    maybe_writeable = [client, server]

    can_read, can_write, _ = select.select(maybe_readable, maybe_writeable, [], 0)
    print(can_read)
    print(can_write)
    print('---------------------------')

    """
    当client close时, server会收到可写事件, 如果recv内容为空,那么表示client 关闭了连接
    
    """
    client.close()
    maybe_readable.remove(client)
    maybe_writeable.remove(client)
    can_read, can_write, _ = select.select(maybe_readable, maybe_writeable, [], 0)
    print(can_read)
    print(can_write)
    print('---------------------------')
    print(server.recv(1024))


if __name__ == '__main__':
    test_client_close()
