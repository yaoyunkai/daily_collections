"""

>>> f = open('sample.txt','w')
>>> f
<_io.TextIOWrapper name='sample.txt' mode='w' encoding='UTF-8'>
>>> f.buffer
<_io.BufferedWriter name='sample.txt'>
>>> f.buffer.raw
<_io.FileIO name='sample.txt' mode='wb'>


Created at 2023/3/27
"""
import io
import sys
import urllib.request
from socket import socket, AF_INET, SOCK_STREAM


def func1():
    u = urllib.request.urlopen("https://www.python.org")
    f = io.TextIOWrapper(u, encoding='utf8')
    text = f.read()
    print(text)


def func2():
    print(sys.stdout.encoding)
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='latin-1')
    print(sys.stdout.encoding)


def echo_client(client_sock, addr):
    print('Got connection from', addr)

    # Make text-mode file wrappers for socket reading/writing
    client_in = open(client_sock.fileno(), 'rt', encoding='latin-1',
                     closefd=False)

    client_out = open(client_sock.fileno(), 'wt', encoding='latin-1',
                      closefd=False)

    # Echo lines back to the client using file I/O
    for line in client_in:
        client_out.write(line)
        client_out.flush()

    client_sock.close()


def echo_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)
    while True:
        client, addr = sock.accept()
        echo_client(client, addr)


if __name__ == '__main__':
    func2()
