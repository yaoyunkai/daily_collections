"""


Created at 2023/4/8
"""

from collections import namedtuple

Coordinate = namedtuple('Coordinate', 'lat lon')

if __name__ == '__main__':
    print(issubclass(Coordinate, tuple))

    pos1 = Coordinate(55.76, 37.62)
    pos2 = Coordinate(55.76, 37.62)
    print(pos1 == pos2)
    print(pos1 == Coordinate(55.76, 37.62))
