"""
迭代器代替while无限循环

iter 函数一个鲜为人知的特性是它接受一个可选的 callable 对象和一个标记(结尾)值作为输入参数。

Created at 2023/3/27
"""

CHUNK_SIZE = 8192


def process_data(val):
    pass


def reader(s):
    while True:
        data = s.recv(CHUNK_SIZE)
        if data == b'':
            break
        process_data(data)


def reader2(s):
    for chunk in iter(lambda: s.recv(CHUNK_SIZE), b''):
        process_data(chunk)
