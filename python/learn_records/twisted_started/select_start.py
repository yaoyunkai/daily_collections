"""
file: select_start.py
Created by Libyao at 2023/4/13

select


sock.getsockname() 本机地址

create_connection: 对connect的高级包装

可读事件：
    如果未收到任何数据，则表示断开连接
    可以接受新连接时， listen sock 会有可读事件

可写事件：

timeout: None: 阻塞直到事件到达
         0   : 不等待任何新事件


"""

import socket

import select


def func():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('localhost', 0))
    listener.listen(1)

    client = socket.create_connection(listener.getsockname())
    server, addr = listener.accept()

    data = b'xyz'
    client.sendall(data)
    print(server.recv(1024))

    server.sendall(data)
    print(client.recv(1024))


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


if __name__ == '__main__':
    select_start()
