# benchmark.py
#
# A micro benchmark comparing the performance of sending messages into
# a coroutine vs. sending messages into an object


# An object
class GrepHandler(object):
    def __init__(self, pattern, target):
        self.pattern = pattern
        self.target = target

    def send(self, li):
        if self.pattern in li:
            self.target.send(li)


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.send(None)
        return cr

    return start


@coroutine
def grep(pattern, target):
    while True:
        li = (yield)
        if pattern in li:
            target.send(li)


# A null-sink to send data
@coroutine
def null():
    while True:
        item = (yield)


if __name__ == '__main__':
    from timeit import timeit

    # A benchmark
    line = 'python is nice'
    p1 = grep('python', null())  # Coroutine
    p2 = GrepHandler('python', null())  # Object
    print("coroutine:", timeit("p1.send(line)", "from __main__ import line, p1"))
    print("object:", timeit("p2.send(line)", "from __main__ import line, p2"))
