"""


Created at 2023/3/30
"""

from collections.abc import Iterable


def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x


if __name__ == '__main__':
    items1 = [1, 2, [3, 4, [5, 6], 7], 8]

    # Produces 1 2 3 4 5 6 7 8
    for i in flatten(items1):
        print(i)

    items2 = ['Dave', 'Paula', ['Thomas', 'Lewis']]
    for i in flatten(items2):
        print(i)
