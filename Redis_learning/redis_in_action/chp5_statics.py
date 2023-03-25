"""
使用 Redis 存储统计数据


Create at 2023/3/16 22:50
"""
import contextlib
import math
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


def _get_stddev(sumsq, sum_var, count):
    # 标准差 = sqrt [ (样本平方和 - (样本总和)^2 / 样本个数) / (样本个数 - 1) ]
    variance = (sumsq - (sum_var ** 2) / count) / (count - 1)
    return math.sqrt(variance)


def get_stats(conn: redis.Redis, context, types):
    destination = 'stats:{}:{}'.format(context, types)

    _result = {}

    # return a list of tuple, k is bytes , v is float
    data = conn.zrange(destination, 0, -1, withscores=True)
    if not data:
        return _result

    for _k, _v in data:
        _result[_k.decode('utf8')] = _v

    _result['average'] = _result['sum'] / _result['count']
    if _result['count'] < 1.0:
        return _result

    _result['stddev'] = _get_stddev(_result['sumsq'], _result['sum'], _result['count'])
    return _result


@contextlib.contextmanager
def access_time(conn: redis.Redis, context):
    start = time.time()
    yield

    delta = time.time() - start
    stats = update_stats(conn, context, 'accessTime', delta)
    average = stats[1] / stats[0]

    pipe = conn.pipeline(True)
    pipe.zadd('slowest:accessTime', {context: average})
    # 保留一百个最慢的context
    pipe.zremrangebyrank('slowest:accessTime', 0, -101)
    pipe.execute()


def process_view_hello_world(request):
    conn = redis.Redis()  # or get a conn pool

    with access_time(conn, 'view_hello_world'):
        print('do request and get result, request path: {}'.format(request))
        # time.sleep(0.04)
        resp = '200 ok'

    return resp


if __name__ == '__main__':
    rd = redis.Redis(encoding='utf8')

    # values = [6.7, 6, 7.8, 5.6, 7, 5.8, 7.6, 9, 6.9, 6.8]
    # for val in values:
    #     update_stats(rd, 'UserInfo', 'accessTime', val)

    # values = [9.835, 9.244, 7.567, 6.289, 5.184, 7.003, 5.701, 9.479, 9.786, 5.923,
    #           7.242, 8.097, 9.184, 5.981, 9.301, 6.928, 7.216, 8.569, 6.305, 6.995,
    #           9.846, 7.857, 6.799, 8.835, 7.001, 9.137, 6.982, 6.122, 6.985, 7.246,
    #           6.106, 6.144, 7.756, 9.123, 6.789, 6.911, 8.712, 7.229, 9.025, 8.926,
    #           5.888, 7.796, 8.094, 7.006, 5.824, 9.755, 5.104, 5.392, 5.254, 7.783,
    #           9.369, 5.684, 5.129, 6.538, 5.612]

    # # for val in values:
    # ret1 = update_stats(rd, 'Demo', 'accessTime', )
    # print(ret1)

    process_view_hello_world('hhhh')

    # ret = get_stats(rd, 'Demo', 'accessTime')
    # print(ret)
