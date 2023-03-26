"""
Load Script


Create at 2023/3/26 21:23
"""
import math
import time
import uuid

import redis


def script_load(script):
    sha = [None]

    def call(conn, keys=None, args=None, force_eval=False):
        if keys is None:
            keys = []
        if args is None:
            args = []

        if not force_eval:
            if not sha[0]:
                sha[0] = conn.execute_command("SCRIPT", "LOAD", script, parse="LOAD")

            try:
                return conn.execute_command("EVALSHA", sha[0], len(keys), *(keys + args))

            except redis.exceptions.ResponseError as msg:
                if not msg.args[0].startswith("NOSCRIPT"):
                    raise

        return conn.execute_command("EVAL", script, len(keys), *(keys + args))

    return call


def acquire_lock_with_timeout(conn, lockname, acquire_timeout=10, lock_timeout=10):
    identifier = str(uuid.uuid4())
    lockname = 'lock:' + lockname
    lock_timeout = int(math.ceil(lock_timeout))

    acquired = False
    end = time.time() + acquire_timeout
    while time.time() < end and not acquired:
        acquired = acquire_lock_with_timeout_lua(conn, [lockname], [lock_timeout, identifier]) == b'OK'

        time.sleep(.001 * (not acquired))

    return acquired and identifier


acquire_lock_with_timeout_lua = script_load('''
if redis.call('exists', KEYS[1]) == 0 then 
    return redis.call('setex', KEYS[1], unpack(ARGV))
end
''')


def release_lock(conn, lockname, identifier):
    lockname = 'lock:' + lockname
    return release_lock_lua(conn, [lockname], [identifier])


release_lock_lua = script_load('''
if redis.call('get', KEYS[1]) == ARGV[1] then  
    return redis.call('del', KEYS[1]) or true  
end
''')
