"""
当打开的文件内容有变化时，相应的程序也会有变化


Created at 2023/4/4
"""
import io
import time


def tail_f():
    fp = open('repos.txt', mode='r', encoding='utf8')
    fp.seek(0, io.SEEK_END)
    while True:
        li = fp.readline()
        if not li:
            time.sleep(0.1)
            continue
        print(li)


if __name__ == '__main__':
    tail_f()
