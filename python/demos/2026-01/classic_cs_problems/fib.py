"""
write your description here.

斐波那契数列

"""

from functools import lru_cache
from typing import Generator


@lru_cache(maxsize=None)
def fib4(n: int) -> int:
    if n < 2:
        return n
    return fib4(n - 2) + fib4(n - 1)


def fib5(n: int) -> int:
    if n == 0:
        return n
    last = 0
    next_ = 1

    for _ in range(1, n):
        last, next_ = next_, last + next_

    return next_


def fib6(n: int) -> Generator[int, None, None]:
    yield 0  # special case
    if n > 0:
        yield 1  # special case
    last: int = 0  # initially set to fib(0)
    next_: int = 1  # initially set to fib(1)
    for _ in range(1, n):
        last, next_ = next_, last + next_
        yield next_  # main generation step


if __name__ == '__main__':
    print(fib4(10))
    print(fib4(100))
    print(fib5(100))
