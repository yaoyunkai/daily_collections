"""


Created at 2023/4/15
"""

import errno
import socket

from select_reactor import Reactor


class BuffersWrites(object):

    def __init__(self, data_to_write, on_completion):
        self._buffer = data_to_write
        self._on_completion = on_completion

    def buffering_write(self, reactor: Reactor, sock: socket.socket):
        if self._buffer:
            try:
                written = sock.send(self._buffer)
            except socket.error as e:
                if e.errno != errno.EAGAIN:
                    raise
                return
            else:
                # when send success
                print('sock: {}, wrote: {} bytes'.format(sock.fileno(), written))
                self._buffer = self._buffer[written:]
        if not self._buffer:
            reactor.remove_writer(sock)
            self._on_completion(reactor, sock)


DATA = [b'*', b'*']


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


def write(reactor: Reactor, sock: socket.socket):
    writer = BuffersWrites(b''.join(DATA), write)
    reactor.add_writer(sock, writer.buffering_write)

    print('Client buffering {} bytes to write'.format(len(DATA)))
    DATA.extend(DATA)


if __name__ == '__main__':
    listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen.bind(('localhost', 0))
    listen.listen(1)

    client = socket.create_connection(listen.getsockname())
    client.setblocking(False)

    loop = Reactor()
    loop.add_writer(client, write)
    loop.add_reader(listen, accept)
    loop.run()
