"""

Problems
持有锁的进程因为操作时间过长而导致锁被自动释放，但进程本身并不知晓这一点，还有可能错误地释放其他进程持有的锁

一个持有锁并打算执行长时间操作的进程已经崩溃，但其他想要获取锁的进程不知道哪个进程持有锁，也无法
知道持有锁的进程已经崩溃，只能等待锁释放

在一个进程持有的锁过期后，其他多个进程同时尝试获取锁，并且都获取到了锁

一三种情况同时出现，导致有多个进程获取了锁，而且每个进程都以为自己是唯一一个获得锁的进程


Create at 2023/3/20 22:20
"""
import math
import time
import uuid

import redis


# ------------------- V1 -------------------------

def acquire_lock(conn: redis.Redis, lockname, acquire_timeout=10):
    identifier = str(uuid.uuid4())

    end = time.time() + acquire_timeout
    while time.time() < end:
        if conn.setnx('lock:' + lockname, identifier):
            return identifier

        time.sleep(.001)

    return False


def release_lock(conn: redis.Redis, lockname, identifier):
    pipe = conn.pipeline(True)
    lockname = 'lock:' + lockname

    while True:
        try:
            pipe.watch(lockname)
            if pipe.get(lockname) == identifier:
                pipe.multi()
                pipe.delete(lockname)
                pipe.execute()
                return True

            pipe.unwatch()
            break
        except redis.exceptions.WatchError:
            pass
    return False


def acquire_lock_with_timeout(conn: redis.Redis, lockname, acquire_timeout=10, lock_timeout=10):
    # 128位随机标识符。
    identifier = str(uuid.uuid4())
    lockname = 'lock:' + lockname
    # 确保传给EXPIRE的都是整数。
    lock_timeout = int(math.ceil(lock_timeout))

    end = time.time() + acquire_timeout
    while time.time() < end:
        # 获取锁并设置过期时间。
        if conn.set(lockname, identifier, ex=lock_timeout, nx=True):
            return identifier

        # if conn.setnx(lockname, identifier):
        #     conn.expire(lockname, lock_timeout)
        #     return identifier

        # 检查过期时间，并在有需要时对其进行更新。
        # elif not conn.ttl(lockname):
        #     conn.expire(lockname, lock_timeout)

        time.sleep(.001)

    return False
