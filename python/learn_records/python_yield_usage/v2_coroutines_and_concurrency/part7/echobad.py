"""
A flawed implementation of an concurrent echo server using our task scheduler.

"""

from socket import *

from pyos6 import *


def handle_client(client, addr):
    print(f'Connection from {addr}')
    while True:
        data = client.recv(65536)
        if not data:
            break
        client.send(data)
    client.close()
    print("Client Closed")
    yield


def server(port):
    print("Server Starting")
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('localhost', port))
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        yield NewTask(handle_client(client, addr))


def alive():
    while True:
        print("i am alive")
        yield


if __name__ == '__main__':
    sched = Scheduler()
    sched.new(alive())
    sched.new(server(16000))
    sched.mainloop()
