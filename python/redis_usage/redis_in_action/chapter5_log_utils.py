"""

使用redis记录日志

time-sensitive log

recent log message


Create at 2023/3/15 22:01
"""
import logging
import random
import time
from datetime import datetime
from typing import Any

import faker
import redis

# 设置一个字典，它可以帮助我们将大部分日志的安全级别转换成某种一致的东西。
SEVERITY = {
    logging.DEBUG: 'debug',
    logging.INFO: 'info',
    logging.WARNING: 'warning',
    logging.ERROR: 'error',
    logging.CRITICAL: 'critical',
    'debug': 'debug',
    'info': 'info',
    'warning': 'warning',
    'error': 'error',
    'critical': 'critical',
}


def generate_message(fake: faker.Faker):
    return fake.sentence()


def generate_name(fake: faker.Faker):
    return fake.name()


def log_recent(conn: redis.Redis, name, message, severity: Any = logging.INFO, pipe=None):
    severity = str(SEVERITY.get(severity, 'info')).lower()
    dest_key = 'recent:{}:{}'.format(name, severity)
    message = time.asctime() + ' ' + message

    pipe = pipe or conn.pipeline()
    pipe.lpush(dest_key, message)
    pipe.ltrim(dest_key, 0, 99)
    pipe.execute()


def log_common(conn, name, message, severity: Any = logging.INFO, timeout=5):
    # 设置日志的级别。
    severity = str(SEVERITY.get(severity, 'info')).lower()
    # 负责存储最新日志的键。
    dest_key = 'common:%s:%s' % (name, severity)
    # 因为程序每小时需要轮换一次日志，所以它使用一个键来记录当前所处的小时数。
    start_key = dest_key + ':start'  # common:func1:info:start
    pipe = conn.pipeline()
    end = time.time() + timeout

    while time.time() < end:
        try:
            # 对记录当前小时数的键进行监视，确保轮换操作可以正确地执行。
            pipe.watch(start_key)
            # 取得当前时间。
            now = datetime.utcnow().timetuple()

            # 取得当前所处的小时数。TODO 只要更改这里的获取方式就可以更新log_common的刷新频率
            hour_start = datetime(*now[:4]).isoformat()  # 2020-09-09 10:

            existing = pipe.get(start_key)  # bytes: 2020-09-09 10:
            # 创建一个事务。
            pipe.multi()
            # 如果目前的常见日志列表是上一个小时的……
            if existing and str(existing) < hour_start:
                # ……那么将旧的常见日志信息进行归档。
                pipe.rename(dest_key, dest_key + ':last')
                pipe.rename(start_key, dest_key + ':pstart')
                # 更新当前所处的小时数。
                pipe.set(start_key, hour_start)
            elif not existing:
                pipe.set(start_key, hour_start)

            # 对记录日志出现次数的计数器执行自增操作。
            pipe.zincrby(dest_key, 1, message)
            # log_recent()函数负责记录日志并调用execute()函数。
            log_recent(pipe, name, message, severity, pipe)
            return
        except redis.exceptions.WatchError:
            # 如果程序因为其他客户端在执行归档操作而出现监视错误，那么重试。
            continue


if __name__ == '__main__':
    rd = redis.Redis()
    fk = faker.Faker()

    # name = generate_name(fk)
    # name2 = generate_name(fk)
    # for i in range(10000):
    #     if i % 2 == 0:
    #         log_recent(
    #             rd, name, generate_message(fk)
    #         )
    #     else:
    #         log_recent(
    #             rd, name2, generate_message(fk)
    #         )

    # demo_messages = ['Write keep century by material medical.',
    #                  'She radio study set relate.',
    #                  'Ability attack mission until near.',
    #                  'Evidence sort ask recent two after.',
    #                  'Growth at unit enjoy continue gas.',
    #                  'Others shoulder away go present.',
    #                  'People child hard hour open.',
    #                  'Position break decade bring place.',
    #                  'Physical stock myself.',
    #                  'Person letter citizen exactly pretty thank figure.'
    #                  ]
    #
    # for i in range(10000):
    #     log_common(rd, 'func1', random.choice(demo_messages), logging.DEBUG)
