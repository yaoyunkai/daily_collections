"""
file: select_reactor.py
Created by Libyao at 2023/4/13

基于select的事件循环


"""
import socket

import select


class Reactor:
    def __init__(self):
        self._readers = {}
        self._writers = {}

    def add_reader(self, readable, handler):
        self._readers[readable] = handler

    def add_writer(self, writable, handler):
        self._writers[writable] = handler

    def remove_reader(self, readable):
        self._readers.pop(readable, None)

    def remove_writer(self, writable):
        self._writers.pop(writable, None)

    def run(self):
        while self._readers or self._writers:
            can_read, can_write, _ = select.select(self._readers, self._writers, [])  # blocking
            for r in can_read:
                self._readers[r](self, r)
            for w in can_write:
                if w in self._writers:
                    self._writers[w](self, w)


def accept(reactor: Reactor, listener: socket.socket):
    server, _ = listener.accept()
    reactor.add_reader(server, read)  # 表示 server只会注册可读事件


def read(reactor: Reactor, sock: socket.socket):
    data = sock.recv(1024)
    if data:
        print('Server received', len(data), 'bytes.')
    else:
        sock.close()
        print('socket {} closed.'.format(sock.fileno()))
        reactor.remove_reader(sock)


DATA = [b'*', b'*']


def write(reactor: Reactor, sock: socket.socket):
    # sendall 会阻塞程序
    sock.sendall(b''.join(DATA))
    print('socket {} wrote {} bytes.'.format(sock.fileno(), len(DATA)))
    DATA.extend(DATA)


if __name__ == '__main__':
    listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen.bind(('localhost', 0))
    listen.listen(1)

    client = socket.create_connection(listen.getsockname())

    loop = Reactor()
    loop.add_writer(client, write)
    loop.add_reader(listen, accept)
    loop.run()
