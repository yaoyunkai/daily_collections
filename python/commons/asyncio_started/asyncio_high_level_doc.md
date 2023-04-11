# Asyncio High Level API

asyncio 提供一组 **高层级** API 用于:

- 并发地 [运行 Python 协程](https://docs.python.org/zh-cn/3/library/asyncio-task.html#coroutine) 并对其执行过程实现完全控制;
- 执行 [网络 IO 和 IPC](https://docs.python.org/zh-cn/3/library/asyncio-stream.html#asyncio-streams);
- 控制 [子进程](https://docs.python.org/zh-cn/3/library/asyncio-subprocess.html#asyncio-subprocess);
- 通过 [队列](https://docs.python.org/zh-cn/3/library/asyncio-queue.html#asyncio-queues) 实现分布式任务;
- [同步](https://docs.python.org/zh-cn/3/library/asyncio-sync.html#asyncio-sync) 并发代码;

## Runner

`asyncio.run`

```python
async def main():
    await asyncio.sleep(1)
    print('hello')

asyncio.run(main())
```

## 协程与任务

### 协程

通过 async/await 语法来声明 协程 是编写 asyncio 应用的推荐方式。

```python
import asyncio

async def main():
    print('hello')
    await asyncio.sleep(1)
    print('world')

asyncio.run(main())
```

`asyncio.run()` 函数用来运行最高层级的入口点 "main()" 函数

`asyncio.create_task()` 函数用来并发运行作为 asyncio 任务 的多个协程。

```python
import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    return delay


async def main():
    task1 = asyncio.create_task(say_after(1, 'hello'))

    task2 = asyncio.create_task(say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    ret = await task1
    print('task1 result is:', ret)
    await task2

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())

```

### 可等待对象

**Waitable Object**

三种主要类型: 协程，任务， Futute

#### 协程

在本文档中 "协程" 可用来表示两个紧密关联的概念:

- 协程函数: 定义形式为 `async def` 的函数;
- 协程对象: 调用 协程函数 所返回的对象。

#### 任务

任务 被用来“并行的”调度协程

```python
import asyncio

async def nested():
    return 42

async def main():
    # Schedule nested() to run soon concurrently
    # with "main()".
    task = asyncio.create_task(nested())

    # "task" can now be used to cancel "nested()", or
    # can simply be awaited to wait until it is complete:
    await task

asyncio.run(main())
```

#### Future

是一种特殊的 **低层级** 可等待对象，表示一个异步操作的 **最终结果**。

当一个 Future 对象 被等待，这意味着协程将保持等待直到该 Future 对象在其他地方操作完毕。

在 asyncio 中需要 Future 对象以便允许通过 async/await 使用基于回调的代码。

一个很好的返回对象的低层级函数的示例是 [`loop.run_in_executor()`](https://docs.python.org/zh-cn/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor)。

### 创建任务

```python
async def coro():
    pass


# In Python 3.7+
task1 = asyncio.create_task(coro())

# This works in all Python versions but is less readable
task2 = asyncio.ensure_future(coro())

```

### 休眠

```python
import asyncio
import datetime

async def display_date():
    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)

asyncio.run(display_date())
```

### 并发运行任务

`awaitable asyncio.gather(*aws, loop=None, return_exceptions=False)`

```python
import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")

async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )

asyncio.run(main())

# Expected output:
#
#     Task A: Compute factorial(2)...
#     Task B: Compute factorial(2)...
#     Task C: Compute factorial(2)...
#     Task A: factorial(2) = 2
#     Task B: Compute factorial(3)...
#     Task C: Compute factorial(3)...
#     Task B: factorial(3) = 6
#     Task C: Compute factorial(4)...
#     Task C: factorial(4) = 24
```

### Some APIs

```python
# 保护一个 可等待对象 防止其被 取消
asyncio.shield(aw)

# 等待 aw 可等待对象 完成，指定 timeout 秒数后超时
asyncio.wait_for(aw, timeout)

# 并发运行 aws 指定的 可等待对象 并阻塞线程直到满足 return_when 指定的条件
aysncio.wait(aws, *, loop=None, timeout=None, return_when=ALL_COMPLETED)

# 并发地运行 aws 集合中的 可等待对象。返回一个 Future 对象的迭代器。返回的每个 Future 对象代表来自剩余可等待对象集合的最早结果。
asyncio.as_completed(aws, *, loop=None, timeout=None)

# 向指定事件循环提交一个协程。线程安全。
asyncio.run_coroutine_threadsafe(coro, loop)
    # Create a coroutine
    coro = asyncio.sleep(1, result=3)
    # Submit the coroutine to a given loop
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    # Wait for the result with an optional timeout argument
    assert future.result(timeout) == 3


```

### 内省

`asyncio.current_task(loop=None)`

返回当前运行的 Task 实例，如果没有正在运行的任务则返回 None。

`asyncio.all_tasks(loop=None)`

返回事件循环所运行的未完成的 Task 对象的集合。

### Task对象

一个与 Future 类似 的对象，可运行 Python 协程。非线程安全。

Task 对象被用来在事件循环中运行协程。如果一个协程在等待一个 Future 对象，Task 对象会挂起该协程的执行并等待该 Future 对象完成。当该 Future 对象 完成，被打包的协程将恢复执行。

事件循环使用协同日程调度: 一个事件循环每次运行一个 Task 对象。而一个 Task 对象会等待一个 Future 对象完成，该事件循环会运行其他 Task、回调或执行 IO 操作。

```python
async def cancel_me():
    print('cancel_me(): before sleep')

    try:
        # Wait for 1 hour
        await asyncio.sleep(3600)
    except asyncio.CancelledError:
        print('cancel_me(): cancel sleep')
        raise
    finally:
        print('cancel_me(): after sleep')

async def main():
    # Create a "cancel_me" Task
    task = asyncio.create_task(cancel_me())

    # Wait for 1 second
    await asyncio.sleep(1)

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("main(): cancel_me is cancelled now")

asyncio.run(main())

# Expected output:
#
#     cancel_me(): before sleep
#     cancel_me(): cancel sleep
#     cancel_me(): after sleep
#     main(): cancel_me is cancelled now
```

## Stream

