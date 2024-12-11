"""


Created at 2023/4/8
"""
import typing
from collections import namedtuple

Coordinate = namedtuple('Coordinate', 'lat lon')


class DemoNTClass(typing.NamedTuple):
    a: int
    b: float = 1.1
    c = 'spam'


def run_namedtuple():
    print(DemoNTClass.__annotations__)
    print(DemoNTClass.a)
    print(DemoNTClass.b)

    print(DemoNTClass.__doc__)


if __name__ == '__main__':
    # print(issubclass(Coordinate, tuple))
    #
    # pos1 = Coordinate(55.76, 37.62)
    # pos2 = Coordinate(55.76, 37.62)
    # print(pos1 == pos2)
    # print(pos1 == Coordinate(55.76, 37.62))

    run_namedtuple()
