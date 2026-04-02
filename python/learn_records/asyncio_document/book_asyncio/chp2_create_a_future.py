"""
Future ，表示在未来某个时间点获得但目前可能还不存在的值。

"""

from asyncio import Future


def create_future():
    my_future = Future()

    print(f"Is my_future done? {my_future.done()}")

    my_future.set_result(42)

    print(f"Is my_future done? {my_future.done()}")
    print(f"What is the result of my_future? {my_future.result()}")


if __name__ == "__main__":
    create_future()
