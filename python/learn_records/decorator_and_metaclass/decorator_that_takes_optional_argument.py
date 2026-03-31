"""


Created at 2023/3/27
"""

import logging
from functools import partial, wraps
from typing import Callable, Optional


def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    if func is None:
        return partial(logged, level=level, name=name, message=message)

    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.log(level, logmsg)
        return func(*args, **kwargs)

    return wrapper


# Example use
@logged
def add(x, y):
    return x + y


"""
add = logged(add)
这时候，被装饰函数会被当做第一个参数直接传递给 logged 装饰器。 
因此，logged() 中的第一个参数就是被包装函数本身。所有其他参数都必须有默认值。


"""


@logged(level=logging.CRITICAL, name="example")
def spam():
    print("Spam!")


"""
spam = logged(level=logging.CRITICAL, name='example')(spam)


"""


def deco(func: Optional[Callable] = None, *, num: int = 1) -> Callable:

    # @deco(num=3)
    if func is None:
        return partial(deco, num=num)

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"--- 装饰器启动，当前 num 的值为: {num} ---")
        result = None
        for i in range(num):
            print(f"执行第 {i + 1} 次...")
            result = func(*args, **kwargs)

        return result

    return wrapper


@deco
def say_hello(name: str) -> None:
    """
    say_hello = deco(say_hello)

    """
    print(f"Hello, {name}!")


@deco(num=3)
def say_hi(name: str) -> None:
    print(f"Hi, {name}!")


if __name__ == "__main__":
    print("测试无参装饰器：")
    say_hello("Alice")

    print("\n测试有参装饰器：")
    say_hi("Bob")
