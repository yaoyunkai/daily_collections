"""
02_create_non_blocking_socket.py


created at 2026-04-07
"""

import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 8091))
server_socket.listen()
server_socket.setblocking(False)


def client_handle(conn: socket.socket):
    local_ip, local_port = conn.getsockname()
    print(f"这个 conn 的本地端是: {local_ip}:{local_port}")
    remote_ip, remote_port = conn.getpeername()
    print(f"这个 conn 的远程端是: {remote_ip}:{remote_port}")

    buffer = b""

    while buffer[-2:] != b"\r\n":
        data = conn.recv(2)
        if not data:
            break
        else:
            print(f"I got data: {data}!")
            buffer = buffer + data

    print(f"All the data is: {buffer}")

    conn.send(buffer)
    conn.close()


try:
    print("Server is running... Press Ctrl+C to stop.")
    while True:
        try:
            connection, client_address = server_socket.accept()
            connection.setblocking(False)
            print(f"I got a connection from {client_address}!")

            t = threading.Thread(target=client_handle, args=(connection,), daemon=True)
            t.start()

        except socket.timeout:
            continue

except KeyboardInterrupt:
    print("\n[!] Ctrl+C detected! Shutting down the server immediately...")

finally:
    server_socket.close()
    print("Server socket closed.")
