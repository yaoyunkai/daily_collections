# echoserver2.py
#
# A concurrent echo server using coroutines

from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, socket

from pyos8 import NewTask, Scheduler
from sockwrap import Socket


def handle_client(client, addr):
    print("Connection from", addr)
    while True:
        data = yield client.recv(65536)
        if not data:
            break
        yield client.send(data)
    print("Client closed")
    yield client.close()


def server(port):
    print("Server starting")
    rawsock = socket(AF_INET, SOCK_STREAM)
    rawsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    rawsock.bind(("", port))
    rawsock.listen(1024)

    sock = Socket(rawsock)
    while True:
        client, addr = yield sock.accept()
        yield NewTask(handle_client(client, addr))


if __name__ == '__main__':
    sched = Scheduler()
    sched.new(server(45000))
    sched.mainloop()
