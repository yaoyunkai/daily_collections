"""


Create at 2023/3/26 22:00
"""
import re

line = 'asdf fjdk; afed, fjek,asdf, foo'


def func1():
    result = re.split(r'[;,\s]\s*', line)
    print(result)


def func2():
    """
    当你使用 re.split() 函数时候，需要特别注意的是正则表达式中是否包含一个括号捕获分组。
    如果使用了捕获分组，那么被匹配的文本也将出现在结果列表中。

    :return:
    """

    fields = re.split(r'(;|,|\s)\s*', line)
    print(fields)


if __name__ == '__main__':
    func2()
