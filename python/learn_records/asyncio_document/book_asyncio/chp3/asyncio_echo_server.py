"""
asyncio_echo_server.py


created at 2026-04-08
"""

from __future__ import annotations

import asyncio
import socket
import typing

if typing.TYPE_CHECKING:
    from asyncio import AbstractEventLoop


async def echo(connection: socket.socket, loop: AbstractEventLoop) -> None:
    try:
        # 当按下enter时，client将数据发回服务端
        while data := await loop.sock_recv(connection, 1024):
            print(f"Received raw data: {repr(data)}")
            if data == b"boom\r\n":
                raise Exception("Unexpected network error")
            await loop.sock_sendall(connection, data)
    except Exception as e:
        pass
    finally:
        connection.close()


async def listen_for_connection(sock: socket.socket, loop: AbstractEventLoop):
    while True:
        conn, address = await loop.sock_accept(sock)
        conn.setblocking(False)
        print(f"Got a connection from {address}")
        asyncio.create_task(echo(conn, loop))


async def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ("127.0.0.1", 8091)
    server_sock.setblocking(False)
    server_sock.bind(server_address)
    server_sock.listen()

    await listen_for_connection(server_sock, asyncio.get_event_loop())


if __name__ == "__main__":
    asyncio.run(main())
