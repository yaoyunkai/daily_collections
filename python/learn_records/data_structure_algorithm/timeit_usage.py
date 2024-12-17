"""


created at 2024/12/17
"""

import timeit


def test2():
    l = []
    for i in range(1000):
        l = l+ [i]


if __name__ == '__main__':
    t1 = timeit.Timer("test2()", "from __main__ import test2")
    print(f'concat {t1.timeit(1000)} ms')
