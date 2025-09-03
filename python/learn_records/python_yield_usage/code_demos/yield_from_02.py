"""

yield from

"""


def sub_gen():
    yield 1.1
    yield 1.2
    return 'done'


def gen():
    yield 1
    result = yield from sub_gen()
    print(f'get result from sub gen: {result}')
    yield 2


if __name__ == '__main__':
    for x in gen():
        print(x)
