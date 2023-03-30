"""
生成器 generator

当遇到return语句时，控制就像在任何函数return中一样，执行适当的finally子句(如果存在的话)。
然后抛出StopIteration异常，表示迭代器已耗尽。
如果控制流离开生成器的末端而没有显式返回，则还会引发StopIteration异常。

Created at 2023/3/30
"""


def fib(max_num):
    n, a, b = 0, 0, 1
    while n < max_num:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'


# 定义函数
def triangles():
    l_range = [1]
    yield l_range
    while True:
        l_range = [v + w for v, w in zip([0] + l_range, l_range + [0])]
        yield l_range


def print_sanjiao():
    # 打印三角
    for i, row in enumerate(triangles()):
        print(row)
        if i >= 10:
            break


if __name__ == '__main__':
    print_sanjiao()
