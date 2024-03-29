# sockwrap.py
#
# Coroutine wrapper around a socket object

from pyos8 import ReadWait, WriteWait


class Socket(object):
    def __init__(self, sock):
        self.sock = sock

    def accept(self):
        yield ReadWait(self.sock)
        client, addr = self.sock.accept()
        yield Socket(client), addr

    def send(self, buffer):
        while buffer:
            yield WriteWait(self.sock)
            length = self.sock.send(buffer)
            buffer = buffer[length:]

    def recv(self, maxbytes):
        yield ReadWait(self.sock)
        yield self.sock.recv(maxbytes)

    def close(self):
        yield self.sock.close()
