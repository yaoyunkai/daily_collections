"""

timezone ?

get current week number ?

time format: https://en.wikipedia.org/wiki/ISO_8601


created at 2024/12/11
"""
from datetime import datetime


def formatted_seconds(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return '{}:{:02d}:{:02d}'.format(h, m, s)


def datetime_to_string(val: datetime):
    """
    convert datetime to string.

    """
    return val.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    print(formatted_seconds(343244554))
