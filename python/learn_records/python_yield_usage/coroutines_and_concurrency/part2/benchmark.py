"""

Benchmark from coroutine and object

"""

from coroutine import coroutine


class GrepHandler(object):
    def __init__(self, pattern, target):
        self.pattern = pattern
        self.target = target

    def send(self, line):
        if self.pattern in line:
            self.target.send(line)


@coroutine
def grep(pattern, target):
    while True:
        line = (yield)
        if pattern in line:
            target.send(line)


@coroutine
def null():
    while True:
        item = yield


if __name__ == '__main__':
    line = 'python is nice'
    p1 = grep('python', null())
    p2 = GrepHandler('python', null())
    from timeit import timeit

    print("coroutine:", timeit("p1.send(line)", "from __main__ import line, p1"))
    print("object:", timeit("p2.send(line)", "from __main__ import line, p2"))
