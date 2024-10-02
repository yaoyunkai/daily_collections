"""
document for throw_dice.py


created at 2024/9/11 16:57
"""
import random


def get_result():
    expect = {1, 2, 3, 4, 5, 6}
    count = 0
    while True:
        if len(expect) == 0:
            break
        num = random.randint(1, 6)
        count += 1
        expect.discard(num)
    return count


if __name__ == '__main__':
    _sum, _cnt = 0, 0

    for i in range(10_0000):
        _cnt += 1
        _sum += get_result()

    print(_sum / _cnt)
