Python Asyncio Book.

# python socket 的 timeout选项

纯阻塞模式 (Blocking)：默认状态。死等，直到有数据或者有连接。
设置方法：sock.setblocking(True) 或 sock.settimeout(None)


纯非阻塞模式 (Non-blocking)：绝不等。如果没有数据，立刻抛出 BlockingIOError 异常。
设置方法：sock.setblocking(False) 或 sock.settimeout(0.0)


超时模式 (Timeout)：介于两者之间的“折中方案”。最多等 N 秒，如果 N 秒内有数据就立刻返回；如果 N 秒后还没数据，抛出 socket.timeout 异常。
设置方法：sock.settimeout(1.0) （只要参数大于 0 就是超时模式）

