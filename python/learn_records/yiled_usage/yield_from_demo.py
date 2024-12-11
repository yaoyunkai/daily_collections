"""

yield from x 表达式对 x 对象所做的第一件事是，调用 iter(x)，从中获取迭代器。 因此，x 可以是任何可迭代的对象。

委派生成器在 yield from 表达式处暂停时，调用方可以直接把数据发给子生成器，子生成器再把产出的值发给调用方。
子生成器返回之后，解释器会抛出 StopIteration 异常，并把返回值附加到异常对象上，此时委派生成器会恢复


概念:

委派生成器:
    包含 yield from <iterable> 表达式的生成器函数。

子生成器:
    从 yield from 表达式中 <iterable> 部分获取的生成器

调用方:
    代调用委派生成器的客户端代码, 客户端



Created at 2023/3/30
"""


def gen1():
    for c in 'AB':
        yield c

    for y in range(1, 4):
        yield y


def gen2():
    yield from 'ABCD'
    yield from range(1, 5)


def chain(*iterable):
    for it in iterable:
        yield from it


if __name__ == '__main__':
    for item in gen1():
        print(item)

    for item in gen2():
        print(item)
