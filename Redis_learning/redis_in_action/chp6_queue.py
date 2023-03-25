"""
队列



Create at 2023/3/22 22:56
"""
import json
import time
import uuid

import redis
from redis.lock import Lock


def send_sold_email_via_queue(conn, seller, item, price, buyer):
    data = {
        'seller_id': seller,
        'item_id': item,
        'price': price,
        'buyer_id': buyer,
        'time': time.time()
    }
    conn.rpush('queue:email', json.dumps(data))


def process_sold_email_queue(conn: redis.Redis):
    while True:
        packed = conn.blpop(['queue:email'], 30)
        if not packed:
            continue

        to_send = json.loads(packed[1])
        try:

            pass
        except Exception as err:
            print("Failed to send sold email", err, to_send)
        else:
            print("Sent sold email", to_send)


def worker_watch_queue(conn, queue, callbacks):
    while True:
        packed = conn.blpop([queue], 30)
        if not packed:
            continue

        name, args = json.loads(packed[1])
        if name not in callbacks:
            print("Unknown callback %s" % name)
            continue
        callbacks[name](*args)


def worker_watch_queues(conn, queues: list, callbacks):
    while True:
        packed = conn.blpop(queues, 30)
        if not packed:
            continue

        name, args = json.loads(packed[1])
        if name not in callbacks:
            print("Unknown callback %s" % name)
            continue
        callbacks[name](*args)


def execute_later(conn, queue, name, args, delay=0):
    identifier = str(uuid.uuid4())
    item = json.dumps([identifier, queue, name, args])
    if delay > 0:
        conn.zadd('delayed:', {item: time.time() + delay})
    else:
        conn.rpush('queue:' + queue, item)
    return identifier


def poll_queue(conn: redis.Redis):
    while True:
        item = conn.zrange('delayed:', 0, 0, withscores=True)
        if not item or item[0][1] > time.time():
            time.sleep(.01)
            continue

        item = item[0][0]
        identifier, queue, function, args = json.loads(item)

        redlock = Lock(conn, 'lock:{}'.format(identifier), blocking_timeout=5)

        # locked = acquire_lock(conn, identifier)
        if not redlock.acquire():
            continue

        if conn.zrem('delayed:', item):
            conn.rpush('queue:' + queue, item)

        redlock.release()
