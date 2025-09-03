"""
生成器


"""


def gen_123():
    yield 1
    yield 2
    yield 3

    return 4


if __name__ == '__main__':
    gen = gen_123()
    # print(gen)
    # print(type(gen))

    for item in gen:
        print(item)
