"""
身份证校验

created at 2025/5/3
"""
import re

number_pattern = re.compile(r'\d{17}[0-9X]')
weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
check_code = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']


def compute_18(value: str):
    if not number_pattern.match(value):
        return False

    value = value[:17]
    count = sum([int(c) * weight[idx] for idx, c in enumerate(value)])
    num = count % 11
    return check_code[num]


if __name__ == '__main__':
    pass
