"""
decorator.py


created at 2026-05-19
"""

import functools
from typing import Callable, Generic, ParamSpec, TypeVar


def print_log(func):
    def wrap(*args, **kwargs):
        print(f"CALLING: {func.__name__}")
        return func(*args, **kwargs)

    return wrap


class PrintLog:
    def __init__(self, func: Callable):
        self.func = func
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        print(f"CALLING: {self.func.__name__}")
        return self.func(*args, **kwargs)


@PrintLog
def foo(x, y):
    print(x + 2 + y)


@print_log
def bar(x):
    print(x - 4)


if __name__ == "__main__":
    foo(4, 8)
    bar(5)
