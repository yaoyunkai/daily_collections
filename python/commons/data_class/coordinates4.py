"""


Created at 2023/4/8
"""

import typing

from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{we}'


if __name__ == '__main__':
    print(issubclass(Coordinate, object))
    print(typing.get_type_hints(Coordinate))

    pos1 = Coordinate(55.76, 37.62)
    pos2 = Coordinate(55.76, 37.62)
    print(pos1 == pos2)
    print(pos1 == Coordinate(55.76, 37.62))
