"""

搜索算法

binary search

hash


created at 2025/4/10
"""

from typing import Sequence


def sequential_search(a_list: Sequence[int, float], item):
    pos = 0
    found = False

    while pos < len(a_list) and not found:
        if a_list[pos] == item:
            found = True
        else:
            pos += 1
    return found


if __name__ == '__main__':
    pass
