"""
Struct的使用

格式化规则

@
=
<
>
!   网络

c    char
i    int
I    unsigned int
l    long
L    unsigned long
N    size_t
e    float 2
f    float 4
d    float 8
s    char[]


Created at 2023/7/19
"""

import struct
import sys

from collections import namedtuple


def endian():
    print(sys.byteorder)


def usage():
    # big endian
    res1 = struct.pack('>h', 1023)
    print(res1)
    # little endian
    res2 = struct.pack('<h', 1023)
    print(res2)

    res3 = struct.pack('>bhl', 1, 2, 3)
    print(res3)

    res4 = struct.pack('@d', 3.1415923)
    print(res4)

    res5 = struct.pack('>f', 3.1415926)
    print(res5)

    res6 = struct.pack('<f', 3.1415926)
    print(res6)


def run_struct():
    record = b'raymond   \x32\x12\x08\x01\x08'

    Student = namedtuple('Student', 'name serialnum school gradelevel')
    stu = Student._make(struct.unpack('<10sHHb', record))
    print(stu)


if __name__ == '__main__':
    endian()
    usage()
    run_struct()
