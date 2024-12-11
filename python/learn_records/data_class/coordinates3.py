"""


Created at 2023/4/8
"""

import typing

Coordinate = typing.NamedTuple('Coordinate', [('lat', float), ('lon', float)])
# Coordinate = typing.NamedTuple('Coordinate', lat=float, lon=float)

if __name__ == '__main__':
    print(issubclass(Coordinate, tuple))
    print(typing.get_type_hints(Coordinate))

    pos1 = Coordinate(55.76, 37.62)
    pos2 = Coordinate(55.76, 37.62)
    print(pos1 == pos2)
    print(pos1 == Coordinate(55.76, 37.62))
