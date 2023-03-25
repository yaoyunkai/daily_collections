"""
Redis 发布与订阅



Create at 2023/3/23 22:56
"""
import redis


def test():
    conn = redis.Redis()
    pubsub = conn.pubsub()
    pubsub.subscribe(['streaming:status:'])

    # {'type': 'subscribe', 'pattern': None, 'channel': b'streaming:status:', 'data': 1}
    # {'type': 'message', 'pattern': None, 'channel': b'streaming:status:', 'data': b'qwerqwerqwer'}
    for item in pubsub.listen():
        print(item)


if __name__ == '__main__':
    test()
