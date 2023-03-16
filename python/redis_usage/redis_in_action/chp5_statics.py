"""
使用 Redis 存储统计数据


Create at 2023/3/16 22:50
"""
import time
import uuid
from datetime import datetime

import redis


def update_stats(conn: redis.Redis, context, types, value, timeout=5):
    destination = 'stats:{}:{}'.format(context, types)

    start_key = destination + ':start'
    pipe = conn.pipeline()
    end = time.time() + timeout

    while time.time() < end:
        try:
            pipe.watch(start_key)
            now = datetime.utcnow().timetuple()
            hour_start = datetime(*now[:4]).isoformat()

            existing = pipe.get(start_key)
            pipe.multi()
            if existing and str(existing) < hour_start:
                pipe.rename(destination, destination + ':last')
                pipe.rename(start_key, destination + ':pstart')
                pipe.set(start_key, hour_start)
            else:
                pipe.set(start_key, hour_start)

            tkey1 = str(uuid.uuid4())
            tkey2 = str(uuid.uuid4())

            pipe.zadd(tkey1, dict(min=value))
            pipe.zadd(tkey2, dict(max=value))

            pipe.zunionstore(destination, [destination, tkey1], aggregate='min')
            pipe.zunionstore(destination, [destination, tkey2], aggregate='max')

            pipe.delete(tkey1, tkey2)

            pipe.zincrby(destination, 1, 'count')
            pipe.zincrby(destination, value, 'sum')
            pipe.zincrby(destination, value * value, 'sumsq')

            return pipe.execute()[-3:]

        except redis.exceptions.WatchError:
            continue


def get_stats(conn: redis.Redis, context, types):
    destination = 'stats:{}:{}'.format(context, types)

    # TODO key is bytes and value is bytes
    data = conn.zrange(destination, 0, -1, withscores=True)

    data[b'average'] = data[b'sum'] / data[b'count']
    numerator = data[b'sumsq'] - ((data[b'sum'] ** 2) / data[b'count'])
    data[b'stddev'] = (numerator / (data[b'count'] - 1 or 1)) ** .5
    return data


if __name__ == '__main__':
    rd = redis.Redis()

    # values = [6.7, 6, 7.8, 5.6, 7, 5.8, 7.6, 9, 6.9, 6.8]
    # for val in values:
    #     update_stats(rd, 'UserInfo', 'accessTime', val)

    ret = get_stats(rd, 'UserInfo', 'accessTime')
    print(ret)
