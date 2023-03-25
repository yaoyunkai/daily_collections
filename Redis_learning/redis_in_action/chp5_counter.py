"""
计数器和统计数据

时间序列计数器

Create at 2023/3/15 22:58
"""
import bisect
import time

import redis

# 以秒为单位的计数器精度
PRECISION = [1, 5, 60, 300, 3600, 18000, 86400]


def update_counter(conn: redis.Redis, name, count=1, now=None):
    """
    hash   key:   counter:prec:name
    zset   key:   counter_set:      member:  prec:name

    :param conn:
    :param name:
    :param count:
    :param now:
    :return:
    """
    now = now or time.time()

    pipe = conn.pipeline()
    for prec in PRECISION:
        pnow = int(now / prec) * prec  # 获取当前时间片的开始时间
        hash_key = '{}:{}'.format(prec, name)
        pipe.zadd('counter_set:', {hash_key: 0})
        pipe.hincrby('counter:' + hash_key, pnow, count)
    pipe.execute()


def get_counter(conn: redis.Redis, name, precision):
    hash_key = 'counter:{}:{}'.format(precision, name)

    data = conn.hgetall(hash_key)
    _result = []
    for k, v in data.items():
        _result.append((int(k), int(v)))
    _result.sort()
    return _result


"""
清理旧的计数器:
由于数据结构的问题没办法使用键过期的功能 expire
    counter_set:
    
    在清理的过程中要注意:
    任何时候都可能会有新的计数器被添加进来
    同一时间可能会有多个不同的清理操作在执行
    对于每天只更新一次的计数器来说，以每分钟一次的频率没什么必要
    如果一个计数器不包含任何数据，那么就不应该进行清理


"""

# 要保留的样本数量
SAMPLE_COUNT = 120


def clean_counters(conn: redis.Redis):
    pipe = conn.pipeline(True)
    passes = 0  # 清理操作执行的次数

    while True:
        start = time.time()
        index = 0  # 表示 zset的index 为了获取member
        while index < conn.zcard('counter_set:'):
            # get member
            hash_key_suffix = conn.zrange('counter_set:', index, index)
            index += 1
            if not hash_key_suffix:
                break
            hash_key_suffix = hash_key_suffix[0]  # bytes

            print('------------------------------------------')
            print('get a counter: {}'.format(hash_key_suffix))

            prec = int(hash_key_suffix.partition(b':')[0])
            bprec = int(prec // 60) or 1

            print('passes: {}, prec: {}, bprec: {}'.format(passes, prec, bprec))

            # 清理程序每60秒就会循环一次，所以需要根据计数器的频率来判断是否必要清理
            # passes 表示每分钟的个数，假如及计数器频率是5,那么 5 % 5 的时候就是清理的时机
            # 对于小于60秒的计数器 一定会进行清理
            if passes % bprec:
                continue

            hash_key = 'counter:{}'.format(hash_key_suffix.decode('utf8'))
            cutoff = time.time() - SAMPLE_COUNT * prec
            samples = conn.hkeys(hash_key)
            samples = [int(ii) for ii in samples]
            samples.sort()

            print('counter中的 timestamp: {}'.format(samples))

            remove = bisect.bisect_right(samples, cutoff)
            print('remove index is: {}'.format(remove))
            if remove:
                conn.hdel(hash_key, *samples[:remove])
                if remove == len(samples):
                    try:
                        pipe.watch(hash_key)
                        if not pipe.hlen(hash_key):
                            pipe.multi()
                            pipe.zrem('counter_set:', hash_key_suffix)
                            print('删除一个计数器: {}'.format(hash_key_suffix))
                            pipe.execute()
                            index -= 1
                        else:
                            pipe.unwatch()
                    except redis.exceptions.WatchError:
                        pass
            print('--------------------------------------------\n')

        passes += 1
        duration = min(int(time.time() - start) + 1, 60)
        print('删除操作花费了: {}'.format(duration))
        print('+++++++++++++++++++++++++++++++++++++++++++ \n')

        time.sleep(max(60 - duration, 1))


if __name__ == '__main__':
    rd = redis.Redis()
    # for i in range(10000):
    #     update_counter(rd, 'demo')

    # print(get_counter(rd, 'demo', 60))

    # print(int(b'60:demo'.partition(b':')[0]))

    clean_counters(rd)
