import socket

from genpickle import gen_pickle


def sendto(source, addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)

    for item in gen_pickle(source):
        s.sendall(item)
    s.close()
