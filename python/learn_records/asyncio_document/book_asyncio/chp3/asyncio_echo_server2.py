"""
asyncio_echo_server2.py


created at 2026-04-08
"""

import asyncio


async def handle_echo(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"[+] 接受来自 {addr} 的新连接")

    try:
        while True:
            data = await reader.read(1024)

            if not data:
                break

            message = data.decode().strip()
            print(f"[*] 收到来自 {addr} 的消息: {message!r}")

            if message.lower() in ("quit", "exit"):
                print(f"[-] 收到特定指令 '{message}'，准备关闭与 {addr} 的连接...")
                writer.write("连接即将关闭。再见！\n".encode())
                await writer.drain()
                break

            writer.write(data)
            await writer.drain()

    except ConnectionResetError:
        print(f"[!] 客户端 {addr} 强行断开了连接")
    finally:
        print(f"[-] 正在关闭与 {addr} 的连接")
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_echo, "127.0.0.1", 8091)

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"[*] Echo Server 正在运行，监听地址: {addrs}")
    print("[*] 提示: 客户端发送 'quit' 或 'exit' 可关闭连接。")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] 服务器已手动停止")
