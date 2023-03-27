"""
排列组合的迭代

itertools



Created at 2023/3/27
"""
from itertools import permutations, combinations, combinations_with_replacement


def func1():
    """
    排列

    """
    items = ['a', 'b', 'c']

    for p in permutations(items):
        print(p)

    for p in permutations(items, 2):
        print(p)

    for p in permutations(items, 1):
        print(p)


def func2():
    """
    对于 combinations() 来讲，元素的顺序已经不重要了。
    也就是说，组合 ('a', 'b') 跟 ('b', 'a') 其实是一样的(最终只会输出其中一个)。

    """
    items = ['a', 'b', 'c']

    for p in combinations(items, 3):
        print(p)

    for p in combinations(items, 2):
        print(p)

    for p in combinations(items, 1):
        print(p)


def func3():
    items = ['a', 'b', 'c']

    for p in combinations_with_replacement(items, 2):
        print(p)


if __name__ == '__main__':
    func3()
