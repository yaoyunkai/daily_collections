"""


created at 2025/4/17
"""


def count_digits(n: int):
    if n < 1:
        raise ValueError('must >= 1')

    count = 0

    while n > 0:
        n = n // 10  # 整除10，逐步去掉末位数字
        count += 1
    return count


if __name__ == '__main__':
    print(count_digits(8333))
