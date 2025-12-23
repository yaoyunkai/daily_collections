"""
任务 协程 future awaitable

如果对一个future执行await操作: 暂停，直到future有一个可供使用的值集


"""
import asyncio
from asyncio import Future


def create_future():
    my_future = Future()

    print(f'Is my_future done? {my_future.done()}')

    my_future.set_result(42)

    print(f'Is my_future done? {my_future.done()}')
    print(f'What is the result of my_future? {my_future.result()}')


def make_request():
    fut = Future()
    asyncio.create_task(set_future_value(fut))  # use coro creat a task
    return fut


async def set_future_value(future: Future):
    await asyncio.sleep(1)
    future.set_result(42)


async def main() -> None:
    future = make_request()
    print(f'Is the future done? {future.done()}')
    value = await future
    print(f'Is the future done? {future.done()}')
    print(value)


if __name__ == '__main__':
    asyncio.run(main())
