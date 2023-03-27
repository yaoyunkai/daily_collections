"""
Zip function

https://docs.python.org/zh-cn/3/library/functions.html#zip

Created at 2023/3/27
"""

xpts = [1, 5, 4, 2, 10, 7]
ypts = [101, 78, 37, 15, 62, 99]

for x, y in zip(xpts, ypts):
    print(x, y)
