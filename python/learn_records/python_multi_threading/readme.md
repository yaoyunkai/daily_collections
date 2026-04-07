# python 的多线程

## 1. socket 打断需要等很久

**卡在 `accept()`**：在Windows上，`server_socket.accept()` 是一个底层的阻塞系统调用，它有时会屏蔽掉 `Ctrl+C` 的信号，直到有新的客户端连进来，它才会苏醒并处理退出信号。

```python
import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 8091))
server_socket.listen()

# 【关键修改 1】给 server_socket 设置一个超时时间（例如 1 秒）
server_socket.settimeout(1.0)

def client_handle(conn: socket.socket):
    buffer = b""
    try:
        while buffer[-2:] != b"\r\n":
            data = conn.recv(2)
            if not data:
                break
            else:
                print(f"I got data: {data}!")
                buffer = buffer + data
        print(f"All the data is: {buffer}")
        conn.send(buffer)
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        conn.close()

try:
    print("Server is running... Press Ctrl+C to stop.")
    while True:
        try:
            # 因为设置了 timeout，这里最多阻塞 1 秒就会抛出 timeout 异常
            connection, client_address = server_socket.accept()
            print(f"I got a connection from {client_address}!")
            
            # 【关键修改 2】添加 daemon=True，将其设置为守护线程
            t = threading.Thread(target=client_handle, args=(connection,), daemon=True)
            t.start()
            
        except socket.timeout:
            # 捕获 accept 的超时异常，什么都不做，直接进入下一次循环
            # 这给了 Python 解释器检查 Ctrl+C (KeyboardInterrupt) 的机会
            continue

except KeyboardInterrupt:
    # 捕获 Ctrl+C 信号
    print("\n[!] Ctrl+C detected! Shutting down the server immediately...")

finally:
    server_socket.close()
    print("Server socket closed.")
```

## 2. daemon 守护线程，应该叫后台线程。

在 Linux/Unix 系统中，Daemon 指的是**“后台服务进程”**。比如你常见的 `sshd`、`httpd`、`mysqld`，后面那个字母 `d` 就是 Daemon 的缩写。它们默默在后台运行，不和用户直接交互。

## 3. daemon 和 join一起使用。

**`t.join()` 的含义**：`join` 的字面意思是“加入/汇合”，在代码里的实际作用是**“阻塞主线程，死等子线程结束”**。

经典场景: daemon + join(timeout)

假设你有一个后台一直在下载文件的 Daemon 线程，当用户按下 `Ctrl+C` 时，你不想立刻杀死它（怕文件损坏），你想给它 2 秒钟的时间保存进度。

```python
import threading
import time

def background_task():
    print("后台任务：开始工作...")
    for i in range(5):
        time.sleep(1)
        print(f"后台任务：正在处理第 {i+1} 步...")
    print("后台任务：工作圆满完成！")

# 1. 设置为守护线程 (Daemon)
t = threading.Thread(target=background_task, daemon=True)
t.start()

try:
    # 主线程模拟做一些其他事情
    time.sleep(2)
    print("主线程：我的工作做完了，准备退出。")
    
except KeyboardInterrupt:
    print("\n主线程：收到 Ctrl+C！准备退出。")

finally:
    print("主线程：我最多再等后台任务 2 秒钟...")
    
    # 2. 配合带超时的 join 使用
    t.join(timeout=2.0) 
    
    if t.is_alive():
        print("主线程：2秒到了，后台任务还没做完，不管了，强制拉闸！")
    else:
        print("主线程：后台任务在2秒内自己做完了，完美退出。")
```

## 4. join(timeout) 没有 daemon

`t.join(timeout=2.0)` 的真正意思是：“主线程在这里**最多只等 2 秒**。2 秒一到，主线程就不等了，**主线程自己继续往下执行代码**。但是，那个子线程**依然在后台继续活着、继续运行**！”

假设我们把上面例子里的 `daemon=True` 删掉（即默认的普通线程）。程序的执行轨迹会变成这样：

1. 子线程开始工作，预计需要 5 秒。
2. 主线程睡了 2 秒。
3. 主线程执行 `t.join(timeout=2.0)`，又等了 2 秒。
4. 此时一共过去了 4 秒。子线程还没干完（还差 1 秒）。
5. `join` 的超时时间到了，主线程解除阻塞，往下走，打印出：“主线程：2秒到了，后台任务还没做完，不管了，强制拉闸！”
6. 主线程的代码执行完了，准备退出 Python 程序。
7. 但是！Python 解释器在临死前会检查一下：“哎？还有一个**非守护线程（普通线程）**还活着呢！”
8. 于是，**Python 解释器会强行拦住主线程，不让程序退出，在后台默默地死等**，直到那个子线程把最后 1 秒钟的活干完。

## 5. 正确做法: start , 然后join

先全部 `start`，再全部 `join`

`join()` 的核心机制：它不仅能“等”，还能“秒过”

 `t.join()` 的一个核心特性：

- 如果线程 `t` **还在运行**，主线程就会在这里**卡住（阻塞）**，直到它运行结束。
- 如果线程 `t` **已经运行结束了**，主线程执行到 `t.join()` 时，**不会卡住，而是瞬间通过（耗时 0 秒）**。

```python
import threading
import time

def worker(i):
    print(f"员工 {i} 开始工作...")
    time.sleep(2) # 模拟工作耗时 2 秒
    print(f"员工 {i} 完成！")

# ✅ 正确做法
threads = [] # 用来保存所有的线程对象

# 第一步：让所有子线程全部 start
for i in range(3):
    t = threading.Thread(target=worker, args=(i,))
    t.start()          # 立刻启动
    threads.append(t)  # 把线程对象存入列表，留着备用

print("主线程：任务已全部派发，大家同时开干吧！")

# 第二步：遍历列表，让主线程挨个 join 等待
for t in threads:
    t.join() 

print("主线程：所有人都干完了，下班！")
```

## 6. 不确定线程数量的做法

1. Python 的 `threading` 模块的方法：`enumerate()`。扫描并返回**当前程序中所有还活着的（Alive）线程列表**。

```python
import threading
import time

def client_handle(client_id):
    print(f"  [子线程] 开始服务客户端 {client_id}...")
    time.sleep(3) # 模拟处理数据需要 3 秒
    print(f"  [子线程] 客户端 {client_id} 服务完成！")

try:
    client_count = 0
    print("服务器运行中... 按 Ctrl+C 停止。")
    
    # 模拟一个不断接收新客户端的死循环
    while True:
        time.sleep(1) # 模拟每隔 1 秒来一个新客户
        client_count += 1
        
        # 动态创建线程，不需要存入任何列表！
        t = threading.Thread(target=client_handle, args=(client_count,))
        t.start()

except KeyboardInterrupt:
    print("\n[主线程] 收到 Ctrl+C！停止接收新客户，准备下班。")
    
finally:
    print("[主线程] 正在检查还有没有没干完活的子线程...")
    
    # 获取主线程自己，因为主线程不能 join 自己
    main_thread = threading.current_thread()
    
    # threading.enumerate() 会返回当前所有存活的线程
    for t in threading.enumerate():
        if t is not main_thread: # 排除主线程自己
            print(f"[主线程] 发现还在忙碌的线程 {t.name}，等待它完成...")
            t.join() # 等待这个存活的子线程结束
            
    print("[主线程] 所有子线程都已结束，服务器完美关闭！")
```

2. 在现代 Python 开发中，面对大量且不确定数量的并发任务，最推荐的做法是**放弃手动创建 `threading.Thread`，改用“线程池”**。

```python
import time
from concurrent.futures import ThreadPoolExecutor

def client_handle(client_id):
    print(f"  [线程池工人] 开始服务客户端 {client_id}...")
    time.sleep(3)
    print(f"  [线程池工人] 客户端 {client_id} 服务完成！")

# 创建一个最多容纳 5 个线程的线程池
executor = ThreadPoolExecutor(max_workers=5)

try:
    client_count = 0
    print("服务器运行中... 按 Ctrl+C 停止。")
    
    while True:
        time.sleep(1)
        client_count += 1
        
        # 把任务提交给线程池，不需要管底层是怎么 start 的
        executor.submit(client_handle, client_count)

except KeyboardInterrupt:
    print("\n[主线程] 收到 Ctrl+C！不再接收新任务。")
    
finally:
    print("[主线程] 通知线程池：等待所有正在干活的工人完工...")
    
    # 这一句是魔法！
    # wait=True 表示主线程会在这里阻塞，直到池子里所有任务都执行完毕
    executor.shutdown(wait=True) 
    
    print("[主线程] 线程池已清空，服务器完美关闭！")
```

