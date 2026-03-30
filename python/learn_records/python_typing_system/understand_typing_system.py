"""
python 的类型系统

"""

from binascii import hexlify
from ctypes import string_at
from sys import getsizeof

a = 0b_01010000_01000001_01010100


def run_with_things():
    print(f"a is {a}")
    # print(hexlify(string_at(id(a), getsizeof(a))))

    print_object_source_bytes(a)
    print_object_source_bytes("PAT")
    # print_object_source_bytes(None)
    # print_object_source_bytes(object())
    # print_object_source_bytes(object)


def print_object_source_bytes(obj: object):
    print(hexlify(string_at(id(obj), getsizeof(obj))))


if __name__ == "__main__":
    run_with_things()
