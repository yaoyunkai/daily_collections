"""
Countdown object


"""


class Countdown(object):
    def __init__(self, start: int):
        self._start = start

    def __iter__(self):
        return CountdownIter(self._start)


class CountdownIter:
    def __init__(self, cnt):
        self.cnt = cnt

    def __iter__(self):
        return self

    def __next__(self):
        if self.cnt <= 0:
            raise StopIteration
        res = self.cnt
        self.cnt -= 1
        return res


if __name__ == '__main__':
    for i in Countdown(5):
        print(i)
