"""

对于select来说不论是阻塞还是非阻塞的sock, 都可以注册到select

server socket
    R:  want to accept


把注册的事件可以是class形式的, 这样可以方便保存状态




Created at 2023/4/10
"""
import socket

import select


def _send(sock, data, w):
    def _real_send():
        try:
            sock.sendall(data)
        except Exception:
            sock.close()
            w.pop(sock.fileno())

    return _real_send


def create_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('localhost', 9000))
    server_sock.listen(5)

    read_dict = {}
    write_dict = {}

    read_dict[server_sock.fileno()] = server_sock

    while True:
        print('---------------------------------')

        # blocking的 select
        can_read, can_write, _ = select.select(read_dict, write_dict, [])
        if can_read:
            for h in can_read:
                print('get read event:', h)
                if h == server_sock.fileno():
                    # noinspection PyUnresolvedReferences
                    client_sock, addr = read_dict[h].accept()
                    read_dict[client_sock.fileno()] = client_sock
                else:
                    # read data from client
                    sock = read_dict[h]
                    try:
                        data = sock.recv(1024)
                        if data:
                            write_dict[h] = _send(sock, data, write_dict)
                        else:
                            print('no data')
                    except Exception:
                        sock.close()
                        read_dict.pop(h)

        if can_write:
            for h in can_write:
                print('get write event:', h)
                write_dict[h]()
                write_dict.pop(h)


if __name__ == '__main__':
    create_server()
