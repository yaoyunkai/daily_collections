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

