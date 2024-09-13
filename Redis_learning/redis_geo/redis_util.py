"""


created at 2024/9/13
"""
import time
import typing

import redis

Number = typing.Union[int, float]
Location = typing.Sequence[Number]
POS = typing.Union[str, list[str]]


def get_redis_connection():
    return redis.Redis(
        host='127.0.0.1',
        port=6379,
        db=0,
    )


def geo_add(key: str, pos_name: str, pos_location: Location, redis_conn=None):
    """
    longitude latitude member

    GEOPOS demo Beijing

    return 1 if new member added to db
    """
    if not redis_conn:
        redis_conn = get_redis_connection()

    values = list()
    for item in pos_location:
        if len(values) == 2:
            break
        values.append(item)
    values.append(pos_name)

    result = redis_conn.geoadd(key, values)
    if result == 1:
        print('geo_add success')


def geo_position(key: str, pos_name: POS, redis_conn=None):
    """
    if key is not exists in db, return None instead of tuple

    """
    if not redis_conn:
        redis_conn = get_redis_connection()

    single_return = False

    if type(pos_name) is str:
        single_return = True
        pos_name = [pos_name, ]

    result = redis_conn.geopos(key, *pos_name)
    if single_return:
        return result[0]

    return result


def geo_list(key: str, redis_conn=None):
    """
    get all the position loc of the key

    """
    if not redis_conn:
        redis_conn = get_redis_connection()

    position_list = []
    start = "0"
    end_time = time.time() + 30
    while (time.time() < end_time) and (start != 0):
        start, fetch_items = redis_conn.zscan(key, cursor=start, match='*', count=20, )
        for item, _ in fetch_items:
            position_list.append(item)

    result = geo_position(key, position_list)
    return result


def geo_search(key: str, pos_location: Location, radius: Number, redis_conn=None):
    if not redis_conn:
        redis_conn = get_redis_connection()

    positions = redis_conn.georadius(key,
                                     longitude=pos_location[0],
                                     latitude=pos_location[1],
                                     radius=radius,
                                     unit='km')
    return geo_position(key, positions)


if __name__ == '__main__':
    # geo_add('demo', 'Beijing', (116.20, 39.56))
    # geo_add('demo', 'Shanghai', (121.47, 31.23))
    # geo_add('demo', 'ChangSha', (112.982279, 28.19409))

    geo_list('demo')
