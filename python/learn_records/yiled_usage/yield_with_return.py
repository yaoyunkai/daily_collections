"""
当遇到return语句时，控制就像在任何函数return中一样，执行适当的finally子句(如果存在的话)。
然后抛出StopIteration异常，表示迭代器已耗尽。
如果控制流离开生成器的末端而没有显式返回，则还会引发StopIteration异常。


如果一个未处理的异常(包括但不限于StopIteration)由生成器函数引发或传递，
则该异常将以通常的方式传递给调用者，并且后续尝试恢复生成器函数将引发StopIteration。
换句话说，未处理的异常会终止生成器的使用寿命。


Created at 2023/3/30
"""


def f1():
    try:
        return
    except:
        yield 1


def f2():
    try:
        raise StopIteration
    except:
        yield 42


def f3():
    return 1 / 0


def gen_1():
    yield f3()
    yield 42


def f4():
    try:
        yield 1
        try:
            yield 2
            1 / 0
            yield 3  # never get here
        except ZeroDivisionError:
            yield 4
            yield 5
            raise
        except:
            yield 6
        yield 7  # the "raise" above stops this
    except:
        yield 8
    yield 9
    try:
        x = 12
    finally:
        yield 10
    yield 11


if __name__ == '__main__':
    # print(list(f1()))
    # print(list(f2()))

    # g = gen_1()
    # g.send(None)
    # print(g.gi_code)
    # g.send(123)

    print(list(f4()))
