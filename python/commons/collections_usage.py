"""
Collections

deque



Created at 2023/3/27
"""
from collections import deque


def search(lines, pattern, history=5):
    previous_lines = deque(maxlen=history)
    for _line in lines:
        if pattern in _line:
            yield _line, previous_lines
        previous_lines.append(_line)


# Example use on a file
if __name__ == '__main__':
    with open('somefile.txt') as f:
        for line, prevlines in search(f, 'python', 5):
            for pline in prevlines:
                print(pline, end='')
            print(line, end='')
            print('-' * 20)
