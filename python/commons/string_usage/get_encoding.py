"""

获取文件编码

links:
    https://stackoverflow.com/questions/3298569/difference-between-mbcs-and-utf-8-on-windows
    https://docs.python.org/zh-cn/3/howto/unicode.html

说明:
    文本文件默认使用 locale.getpreferredencoding() 编码

    isatty 表示是否输出到控制台

    cp936 : gbk


locale.getpreferredencoding() -> 'cp936'
                type(my_file) -> <class '_io.TextIOWrapper'>
             my_file.encoding -> 'cp936'
          sys.stdout.isatty() -> False
          sys.stdout.encoding -> 'UTF-8'
           sys.stdin.isatty() -> False
           sys.stdin.encoding -> 'UTF-8'
          sys.stderr.isatty() -> False
          sys.stderr.encoding -> 'UTF-8'
     sys.getdefaultencoding() -> 'utf-8'
  sys.getfilesystemencoding() -> 'utf-8'

Create at 2023/3/29 22:45
"""

import locale  # noqa
import sys  # noqa

expressions = """
        locale.getpreferredencoding()
        type(my_file)
        my_file.encoding
        sys.stdout.isatty()
        sys.stdout.encoding
        sys.stdin.isatty()
        sys.stdin.encoding
        sys.stderr.isatty()
        sys.stderr.encoding
        sys.getdefaultencoding()
        sys.getfilesystemencoding()
    """

my_file = open('dummy', 'w')

for expression in expressions.split():
    value = eval(expression)
    print(expression.rjust(30), '->', repr(value))
