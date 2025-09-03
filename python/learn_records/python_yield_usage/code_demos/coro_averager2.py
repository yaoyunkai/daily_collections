"""

Coro Averager

"""

from collections.abc import Generator
from typing import NamedTuple, TypeAlias


class Result(NamedTuple):
    count: int
    average: float


class Sentinel:
    def __repr__(self):
        return f'<Sentinel>'


STOP = Sentinel()

# SendType = Union[float, Sentinel]
SendType: TypeAlias = float | Sentinel


def averager2(verbose: bool = False) -> Generator[None, SendType, Result]:
    total = 0.0
    count = 0
    average = 0.0

    while True:
        term = yield
        if verbose:
            print('received:', term)
        if isinstance(term, Sentinel):
            break

        total += term
        count += 1
        average = total / count

    return Result(count, average)


def compute():
    res = yield from averager2(True)
    print(f'computed: {res}')
    return res


def run1():
    coro_avg = averager2()
    next(coro_avg)

    coro_avg.send(10)
    coro_avg.send(30)
    coro_avg.send(50)
    try:
        coro_avg.send(STOP)

    except StopIteration as e:
        result = e.value
        print(result)


def run2():
    comp = compute()
    for v in [None, 10, 20, 30, 40, STOP]:
        try:
            comp.send(v)
        except StopIteration as e:
            result = e.value
            print(result)


if __name__ == '__main__':
    run2()
