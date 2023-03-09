"""


Created at 2023/3/9
"""
import redis


def get_conn():
    return redis.Redis()
