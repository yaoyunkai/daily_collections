"""
03_selector_with_socket.py

在单线程异步网络编程中，timeout=1（或者 0.5、0.1）是最标准的写法。

timeout 参数

None,  阻塞直到有事件
0
>0

==================================

conn的 write event


created at 2026-04-07
"""

import selectors
import socket

selector = selectors.DefaultSelector()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.setblocking(False)

server_socket.bind(("localhost", 8091))
server_socket.listen()

selector.register(server_socket, selectors.EVENT_READ)

client_buffers = {}
print("Server is running on port 8091...")


while True:
    events = selector.select(timeout=1)
    if len(events) == 0:
        print("no events")

    for event, _ in events:
        event_socket: socket.socket = event.fileobj

        if event_socket is server_socket:
            conn, client_address = server_socket.accept()
            conn.setblocking(False)
            print(f"I got a connection from {client_address}!")
            selector.register(conn, selectors.EVENT_READ)
            client_buffers[conn] = b""

        else:
            data = event_socket.recv(1024)

            if data:
                client_buffers[event_socket] += data

                if b"\r\n" in client_buffers[event_socket]:
                    complete_message = client_buffers[event_socket]
                    print(f"Got complete message: {complete_message}")

                    event_socket.sendall(complete_message)
                    print("Message sent. Closing connection.")
                    selector.unregister(event_socket)
                    event_socket.close()
                    del client_buffers[event_socket]

            else:
                print("Client disconnected abruptly.")
                selector.unregister(event_socket)
                event_socket.close()

                if event_socket in client_buffers:
                    del client_buffers[event_socket]
