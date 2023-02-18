"""
excepthook 处理未捕获的异常


Created at 2023/2/18
"""

import sys

# a function
# print(sys.excepthook)

tmp = sys.excepthook


def my_hook(exctype, value, traceback):
    print(exctype)  # 异常的类型
    print(value)  # 异常的实例
    print(traceback)  # traceback 对象
    tmp(exctype, value, traceback)


sys.excepthook = my_hook

if __name__ == '__main__':
    0 / 0
