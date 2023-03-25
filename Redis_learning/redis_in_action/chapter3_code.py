"""
基本的事务

Create at 2023/3/12 22:47
"""
import time

import redis


def notrans():
    print(conn.incr('notrans:'))
    time.sleep(0.1)
    conn.incr('notrans:', -1)


def trans():
    pipeline = conn.pipeline()
    pipeline.incr('trans:')
    time.sleep(0.1)
    pipeline.incr('trans:', -1)
    print(pipeline.execute()[0])


if __name__ == '__main__':
    conn = redis.Redis()
