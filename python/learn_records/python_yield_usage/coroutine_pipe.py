"""
Pipeline processing

Source: 驱动方，调用方，一般不是协程

pipeline sink: 必须有终止点

pipeline filter: 过滤器一般包含 recv 和 send

pipeline Branch: 分支，接受一个 yield 数据，并将数据发送给多个 协程

"""

import time


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.send(None)
        return cr

    return start


def follow(thefile, target):
    thefile.seek(0, 2)  # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)  # Sleep briefly
            continue
        target.send(line)


@coroutine
def grep(pattern, target):
    while True:
        line = (yield)  # Receive a line
        if pattern in line:
            target.send(line)  # Send to next stage


# A sink.  A coroutine that receives data

@coroutine
def printer():
    while True:
        line = (yield)
        print(line)


# Example use
if __name__ == '__main__':
    f = open("access-log")
    follow(f, grep('python', printer()))
