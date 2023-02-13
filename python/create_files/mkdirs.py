"""
create dir, and change permission

RWX 421

UGOA: user, group, other, all

https://stackoverflow.com/questions/16249440/changing-file-permission-in-python

"""

import errno
import os
import stat

test_path = 'null'


def func():
    os.chmod(test_path, 0o444)


def create_path(file_path):
    created = False
    folders = [f for f in file_path.split(os.sep) if f]
    for _ in folders:
        try:
            os.makedirs(file_path, mode=0o777)
            created = True
            print('created %r', file_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        try:
            os.chmod(file_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        except OSError as e:
            if e.errno != errno.EPERM:
                raise
    return created


def touch(path):
    with open(path, 'ab'):
        try:
            os.utime(path, None)
            os.chmod(path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH |
                     stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
        except OSError:
            pass


def get_path_permissions(path):
    return oct(stat.S_IMODE(os.stat(path).st_mode))
