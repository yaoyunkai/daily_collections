"""
file_download_demo.py


created at 2026-04-08
"""

import asyncio
import os
import urllib.parse

import aiofiles  # 引入 aiofiles 库

# --- 常量配置 (Constants) ---
HOST = "127.0.0.1"
PORT = 8080
CHUNK_SIZE = 64 * 1024  # 每次读取 64KB
SERVE_DIR = "./download_files"


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr = writer.get_extra_info("peername")
    print(f"[+] 收到来自 {addr} 的连接")

    try:
        request_line = await reader.readline()
        if not request_line:
            return

        req_str = request_line.decode("utf-8").strip()
        parts = req_str.split()
        if len(parts) < 2 or parts[0] != "GET":
            return

        # 解析路径并防止目录穿越
        raw_path = urllib.parse.unquote(parts[1])
        filename = os.path.basename(raw_path)

        if not filename or filename == "/":
            filename = "sample_video.mp4"

        filepath = os.path.join(SERVE_DIR, filename)

        # 消耗剩余 Headers
        while True:
            line = await reader.readline()
            if line == b"\r\n" or not line:
                break

        if not os.path.exists(filepath):
            print(f"[-] 文件未找到: {filepath}")
            response = "HTTP/1.1 404 Not Found\r\nContent-Length: 14\r\n\r\nFile not found"
            writer.write(response.encode("utf-8"))
            await writer.drain()
            return

        # 构造 HTTP 响应头
        file_size = os.path.getsize(filepath)
        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/octet-stream\r\n"
            f'Content-Disposition: attachment; filename="{filename}"\r\n'
            f"Content-Length: {file_size}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        print(f"[*] 开始发送文件: {filename} ({file_size} bytes)")
        writer.write(headers.encode("utf-8"))
        await writer.drain()

        # [核心改动] 使用 aiofiles 异步读取文件并分块发送
        async with aiofiles.open(filepath, "rb") as f:
            while True:
                # 异步等待磁盘读取完成，期间事件循环可以去处理其他客户端
                chunk = await f.read(CHUNK_SIZE)
                if not chunk:
                    break
                writer.write(chunk)
                await writer.drain()  # 异步等待网络写入完成

        print(f"[+] 文件 {filename} 发送完毕")

    except ConnectionResetError:
        print(f"[!] 客户端 {addr} 取消了下载")
    except Exception as e:
        print(f"[!] 发生错误: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"[-] 连接已关闭: {addr}\n")


async def main():
    os.makedirs(SERVE_DIR, exist_ok=True)
    test_file = os.path.join(SERVE_DIR, "sample_video.mp4")

    if not os.path.exists(test_file):
        print("[*] 正在生成 50MB 的测试文件...")
        # [附加改动] 生成测试文件也改为 aiofiles 异步写入
        async with aiofiles.open(test_file, "wb") as f:
            await f.write(os.urandom(50 * 1024 * 1024))

    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[*] HTTP 下载服务器 (aiofiles版本) 已启动，监听 http://{HOST}:{PORT}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] 服务器已关闭")
