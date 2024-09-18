"""


created at 2024/9/13
"""
import typing

import redis

Number = typing.Union[int, float]
Location = typing.Sequence[Number]


def get_redis_connection():
    return redis.Redis(
        host='127.0.0.1',
        port=6379,
        db=0,
    )


def to_str(val: str | bytes):
    if type(val) is bytes:
        return val.decode('utf8', errors='ignore')
    elif type(val) is str:
        return val
    return str(val)


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


def geo_position(key: str, pos_name: str, redis_conn=None):
    """
    if key is not exists in db, return None instead of tuple

    """
    if not redis_conn:
        redis_conn = get_redis_connection()

    # list of tuple / None
    result = redis_conn.geopos(key, pos_name)
    result = result[0]
    return result if result is None else {
        'name': to_str(pos_name),
        'longitude': result[0],
        'latitude': result[1],
    }


def geo_positions(key: str, pos_names: list[str], redis_conn=None):
    """
    only result position if exists

    """
    if not redis_conn:
        redis_conn = get_redis_connection()

    result = redis_conn.geopos(key, *pos_names)

    final_result = []
    for idx, item in enumerate(result):
        if item is not None:
            final_result.append({
                'name': to_str(pos_names[idx]),
                'longitude': item[0],
                'latitude': item[1],
            })
    return final_result


def geo_list(key: str, redis_conn=None):
    """
    get all the position loc of the key

    """
    if not redis_conn:
        redis_conn = get_redis_connection()

    positions = redis_conn.zrange(key, start=0, end=-1)
    if len(positions) == 0:
        return []
    return geo_positions(key, positions, redis_conn=redis_conn)


def geo_search(key: str, pos_location: Location, radius: Number, redis_conn=None):
    if not redis_conn:
        redis_conn = get_redis_connection()

    if len(pos_location) < 2:
        raise ValueError('location must be ...')

    positions = redis_conn.georadius(key,
                                     longitude=pos_location[0],
                                     latitude=pos_location[1],
                                     radius=radius,
                                     unit='km')
    if len(positions) == 0:
        return []
    return geo_positions(key, positions, redis_conn=redis_conn)


if __name__ == '__main__':
    # geo_add('demo', 'Beijing', (116.20, 39.56))
    # geo_add('demo', 'Shanghai', (121.47, 31.23))
    # geo_add('demo', 'ChangSha', (112.982279, 28.19409))
    print(geo_search('loc', (15, 37), 200, ))
