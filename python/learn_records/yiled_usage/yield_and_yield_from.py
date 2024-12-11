"""


Created at 2023/3/30
"""


def f():
    def do_yield(n):
        yield n

    x = 0

    while 1:
        x += 1
        print(x)
        do_yield(x)


def f2():
    def do_yield(n):
        yield n

    x = 0

    while 1:
        x += 1
        print(x)
        yield from do_yield(x)


if __name__ == '__main__':
    f2()
