"""
times tool

"""


def formatted_seconds(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return '{}:{:02d}:{:02d}'.format(h, m, s)


if __name__ == '__main__':
    print(formatted_seconds(343244554))
