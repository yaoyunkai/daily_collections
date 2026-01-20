import io
import time

from coroutine import coroutine

"""

@coroutine
def filter(target):
    while True:
        item = yield
        # do addition actions
        target.send(item)

"""


def follow(file_obj, target):
    file_obj.seek(0, io.SEEK_END)
    while True:
        line = file_obj.readline()
        if not line:
            time.sleep(0.1)
            continue
        target.send(line)


@coroutine
def printer():
    while True:
        line = yield
        print(line)


if __name__ == '__main__':
    fp = open('demo.txt', mode='r', encoding='utf8')
    follow(fp, printer())
