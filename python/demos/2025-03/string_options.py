"""

字符操作

created at 2025/3/15
"""


def insert_space(string: str, n_length: int) -> str:
    if not string:
        return ''
    return ' '.join([string[i:i + n_length] for i in range(0, len(string), n_length)])


if __name__ == '__main__':
    print(insert_space('45673345', 2))
