"""


Created at 2023/3/10
"""

import heapq
import pprint
import random


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def empty(self):
        return len(self._queue) == 0


def make_demos(nums=50):
    printers = ['A', 'B', 'C', 'D', 'E']
    _ret = []

    for _ in range(nums):
        _printer = random.choice(printers)
        _priority = random.randint(0, 10)
        _file_code = random.randint(10000, 99999)

        _ret.append((_printer, _priority, _file_code))

    pprint.pprint(_ret)
    return _ret


_demo1 = [
    # 'A',
    # 'A',
    # 'A',
    ('A', 9, 53809),
    ('A', 10, 1),
    ('A', 2, 4),
    ('A', 3, 6),
    # 'A',
    ('A', 10, 2),
    # 'A',
    # 'A',
    'A',
    ('E', 1, 81532),
    ('D', 6, 53594),
    ('D', 3, 49838),
    ('D', 4, 70039),
    ('A', 3, 29970),
    ('B', 7, 97414),
    ('B', 6, 31095),
    ('E', 3, 78393),
    ('C', 5, 91653),
    ('A', 3, 45179),
    ('E', 1, 86499),
    ('B', 10, 78387),
    ('A', 6, 68472),
    ('C', 4, 40779),
    ('C', 0, 53075),
    ('D', 7, 34831),
    ('B', 1, 77239),
    ('E', 3, 47753),
    ('C', 9, 82814),
    ('B', 2, 41295),
    ('E', 4, 29638),
    ('D', 7, 83693),
    ('E', 3, 29520),
    ('E', 0, 55447),
    ('D', 9, 70812),
    ('B', 2, 85261),
    ('C', 5, 41835),
    ('A', 5, 59072),
    ('A', 6, 29227),
    ('A', 5, 75285),
    ('B', 8, 67634),
    ('C', 1, 63176),
    ('D', 9, 35660),
    ('B', 9, 92786),
    ('A', 1, 68431),
    ('D', 8, 94728),
    ('B', 10, 17191),
    ('B', 4, 92155),
    ('A', 3, 55492),
    ('C', 5, 65802),
    ('C', 1, 82593),
    ('A', 1, 93499),
    ('E', 1, 44483),
    ('D', 7, 19241),
    ('E', 7, 81631),
    ('B', 8, 43218),
    ('E', 9, 12080),
    ('E', 8, 11500),
]


def runner(input_val):
    """
    input_val is a list have below items:
        A 10 333
        B 3  44

        A
        B
    """

    _queue_dict = {}

    for item in input_val:
        if len(item) == 1:
            _printer = item
            _type = 'out'
        else:
            _printer, _priority, _file_code = item
            _type = 'in'

        if _printer not in _queue_dict:
            _queue_dict[_printer] = PriorityQueue()

        if _type == 'in':
            _queue_dict[_printer].push(_file_code, _priority)
        else:
            if _queue_dict[_printer].empty():
                print('NULL')
            else:
                print(_queue_dict[_printer].pop())


if __name__ == '__main__':
    # make_demos()
    runner(_demo1)
