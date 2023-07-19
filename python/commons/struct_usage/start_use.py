"""
Struct的使用


Created at 2023/7/19
"""

from collections import namedtuple
from struct import calcsize
from struct import pack
from struct import unpack


def test_namedtuple():
    record = b'raymond   \x32\x12\x08\x01\x08'
    name, serialnum, school, gradelevel = unpack('<10sHHb', record)

    Student = namedtuple('Student', 'name serialnum school gradelevel')
    Student._make(unpack('<10sHHb', record))


if __name__ == '__main__':
    # to bytes
    print(pack(">bhl", 1, 2, 3))

    # from bytes to tuple of data
    print(unpack('>bhl', b'\x01\x00\x02\x00\x00\x00\x03'))

    # compute size
    print(calcsize('>bhl'))
