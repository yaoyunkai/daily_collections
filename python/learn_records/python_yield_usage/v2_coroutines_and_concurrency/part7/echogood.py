from socket import *

from pyos7 import *


def handle_client(client, addr):
    print("Connection from", addr)
    while True:
        yield ReadWait(client)
        data = client.recv(65536)
        if not data:
            break
        yield WriteWait(client)
        client.send(data)
    client.close()
    print("Client closed")


def server(port):
    print("Server starting")
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(("localhost", port))
    sock.listen(5)
    while True:
        yield ReadWait(sock)
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
