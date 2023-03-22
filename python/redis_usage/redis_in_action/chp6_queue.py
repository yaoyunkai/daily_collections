"""
队列



Create at 2023/3/22 22:56
"""
import json
import time


def send_sold_email_via_queue(conn, seller, item, price, buyer):
    data = {
        'seller_id': seller,  # A
        'item_id': item,  # A
        'price': price,  # A
        'buyer_id': buyer,  # A
        'time': time.time()  # A
    }
    conn.rpush('queue:email', json.dumps(data))  # B


# <start id="_1314_14473_9060"/>
def process_sold_email_queue(conn):
    while True:
        packed = conn.blpop(['queue:email'], 30)  # A
        if not packed:  # B
            continue  # B

        to_send = json.loads(packed[1])  # C
        try:
            fetch_data_and_send_sold_email(to_send)  # D
        except EmailSendError as err:
            log_error("Failed to send sold email", err, to_send)
        else:
            log_success("Sent sold email", to_send)


def worker_watch_queue(conn, queue, callbacks):
    while not QUIT:
        packed = conn.blpop([queue], 30)  # A
        if not packed:  # B
            continue  # B

        name, args = json.loads(packed[1])  # C
        if name not in callbacks:  # D
            log_error("Unknown callback %s" % name)  # D
            continue  # D
        callbacks[name](*args)  # E


def worker_watch_queues(conn, queues, callbacks):  # A
    while not QUIT:
        packed = conn.blpop(queues, 30)  # B
        if not packed:
            continue

        name, args = json.loads(packed[1])
        if name not in callbacks:
            log_error("Unknown callback %s" % name)
            continue
        callbacks[name](*args)


def execute_later(conn, queue, name, args, delay=0):
    identifier = str(uuid.uuid4())  # A
    item = json.dumps([identifier, queue, name, args])  # B
    if delay > 0:
        conn.zadd('delayed:', {item: time.time() + delay})  # C
    else:
        conn.rpush('queue:' + queue, item)  # D
    return identifier  # E


def poll_queue(conn):
    while not QUIT:
        item = conn.zrange('delayed:', 0, 0, withscores=True)  # A
        if not item or item[0][1] > time.time():  # B
            time.sleep(.01)  # B
            continue  # B

        item = item[0][0]  # C
        identifier, queue, function, args = json.loads(item)  # C

        locked = acquire_lock(conn, identifier)  # D
        if not locked:  # E
            continue  # E

        if conn.zrem('delayed:', item):  # F
            conn.rpush('queue:' + queue, item)  # F

        release_lock(conn, identifier, locked)  # G
