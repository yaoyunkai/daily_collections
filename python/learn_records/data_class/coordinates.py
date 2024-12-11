"""


Created at 2023/4/8
"""

import typing


def usage_of_namedtuple():
    Coordinate1 = typing.NamedTuple('Coordinate1', lat=float, lon=float)
    print(typing.get_type_hints(Coordinate1))

    pos0 = Coordinate1(12.34, 12.12)
    print(pos0)

    print(pos0 == Coordinate1(12.34, 12.12))


class Coordinate:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon


if __name__ == '__main__':
    pos1 = Coordinate(55.76, 37.62)
    pos2 = Coordinate(55.76, 37.62)
    print(pos1 == pos2)
    print(pos1 == Coordinate(55.76, 37.62))

    usage_of_namedtuple()
