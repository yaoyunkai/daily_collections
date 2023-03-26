"""

collections:
    OrderedDict
    defaultdict

怎样在数据字典中执行一些计算操作（比如求最小值、最大值、排序等等）？

ZIP 函数的使用
在多个迭代器上并行迭代，从每个迭代器返回一个数据项组成元组。
https://docs.python.org/zh-cn/3/library/functions.html#zip


Created at 2023/3/25
"""
from collections import defaultdict

pairs = {}


def default_dict_usage():
    d = defaultdict(list)
    for key, value in pairs:
        d[key].append(value)


def dict_calc():
    prices = {
        'ACME': 45.23,
        'AAPL': 612.78,
        'IBM': 205.55,
        'HPQ': 37.20,
        'FB': 10.75
    }

    min_price = zip(prices.values(), prices.keys())
    # print(list(min_price))  # 转换为一个list(tuple: (value, key))
    min_price = min(min_price)
    print(min_price)


if __name__ == '__main__':
    dict_calc()
