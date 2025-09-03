"""

生成器的方法
    send
    close


Created at 2023/3/30
"""
from collections import namedtuple
from collections.abc import Generator

Result = namedtuple("Result", 'count average')


def coroutine(func):
    """A decorator that advances
    the execution to the first 'yield'
    in a generator so that this generator
    is "primed".
    """

    def generator(*args, **kwargs):
        primed_func = func(*args, **kwargs)
        primed_func.send(None)
        return primed_func

    return generator


@coroutine
def averager() -> Generator[float, float, None]:
    total = 0.0
    count = 0

    average = None
    while True:
        recv = yield average
        total += recv
        count += 1
        average = total / count


def averager2():
    total = 0.0
    count = 0

    average = None
    while True:
        recv = yield
        if recv is None:
            break

        total += recv
        count += 1
        average = total / count

    return Result(count, average)


if __name__ == '__main__':
    av = averager()
    # next(av)

    av.send(45.6)
    av.send(43.6)
    av.send(41.6)
    av.send(44.6)
    ret = av.send(48.6)
    print(ret)
