"""
Format
https://docs.python.org/zh-cn/3.11/library/string.html#format-string-syntax

为了将整数转换为二进制、八进制或十六进制的文本串， 可以分别使用
bin
oct
hex



Create at 2023/3/26 22:37
"""

x = 1234.567890

print(format(x, '0.2f'))
print(format(x, '>10.1f'))
print(format(x, '<10.1f'))
print(format(x, '^10.1f'))

print(format(x, 'e'))
print(format(x, '0.2E'))
