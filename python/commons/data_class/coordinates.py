"""


Created at 2023/4/8
"""


class Coordinate:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon


if __name__ == '__main__':
    pos1 = Coordinate(55.76, 37.62)
    pos2 = Coordinate(55.76, 37.62)
    print(pos1 == pos2)
    print(pos1 == Coordinate(55.76, 37.62))
