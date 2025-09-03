"""

yield from

"""


def sub_gen():
    yield 1.1
    yield 1.2


def gen():
    yield 1
    yield from sub_gen()
    yield 2


if __name__ == '__main__':
    for x in gen():
        print(x)
