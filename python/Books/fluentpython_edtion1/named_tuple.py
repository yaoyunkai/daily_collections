"""
Collections namedtuple


Created at 2023/3/25
"""

from collections import namedtuple


def func1():
    City = namedtuple('City', 'name country population coordinates')

    tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))

    print(tokyo)
    print(tokyo.name)
    print(tokyo.population)


def func2():
    LatLong = namedtuple('LatLong', 'lat long')
    print(LatLong._fields)

    dt = LatLong._make([28.613889, 77.208889])
    print(dt._asdict())


if __name__ == '__main__':
    func2()
