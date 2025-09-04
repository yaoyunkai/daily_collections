"""

Gen open

"""

import bz2
import gzip

ENCODING = 'utf8'


def gen_open(paths):
    for path in paths:
        if path.suffix == '.gz':
            yield gzip.open(path, 'rt', encoding=ENCODING)
        elif path.suffix == '.bz2':
            yield bz2.open(path, 'rt', encoding=ENCODING)
        else:
            yield open(path, 'rt', encoding=ENCODING)  # as same as r


if __name__ == '__main__':
    pass
