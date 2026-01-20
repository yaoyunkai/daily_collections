import io
import time

from coroutine import coroutine


def follow(file_obj, target):
    file_obj.seek(0, io.SEEK_END)
    while True:
        line = file_obj.readline()
        if not line:
            time.sleep(0.1)
            continue
        target.send(line)


@coroutine
def grep(pattern, target):
    while True:
        line = yield
        if pattern in line:
            target.send(line)


@coroutine
def printer():
    while True:
        line = yield
        print(line)


@coroutine
def broadcast(targets):
    while True:
        item = yield
        for target in targets:
            target.send(item)


if __name__ == '__main__':
    fp = open('demo.txt', mode='r', encoding='utf8')
    follow(fp, broadcast([
        grep('python', printer()),
        grep('java', printer()),
        grep('c', printer()),
    ]))
