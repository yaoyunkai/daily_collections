"""
构建社交程序

数据结构：

lock:<lock_name> 分布式锁

Hash     users: 存储了 username: uid

String   user:id:    生成user id
         status:id:  生成status id

Hash:    user:<uid>   存储用户信息的hash

Hash:    status:<status_id>  存储创建的状态信息

Zset:    home:<uid>     存储了用户主页的时间线(与关注着,被关注着有关)， member: status_id : create time

ZSet:   followers:<uid>      表示关注我的人:   uid: create_time
        following:<uid>      表示我关注的人:   uid: create_time

Zset: profile:<uid>      存储用户发布的状态信息:    status_id : create time



Create at 2023/3/22 21:34
"""
import math
import threading
import time
import uuid

import redis


def to_bytes(x):
    return x.encode() if isinstance(x, str) else x


def to_str(x):
    return x.decode() if isinstance(x, bytes) else x


def acquire_lock_with_timeout(conn, lock_name, acquire_timeout=10, lock_timeout=10):
    identifier = str(uuid.uuid4())
    lock_name = 'lock:' + lock_name
    lock_timeout = int(math.ceil(lock_timeout))

    end = time.time() + acquire_timeout
    while time.time() < end:
        if conn.setnx(lock_name, identifier):
            conn.expire(lock_name, lock_timeout)
            return identifier
        elif conn.ttl(lock_name) < 0:
            conn.expire(lock_name, lock_timeout)
        time.sleep(.001)
    return False


def release_lock(conn, lock_name, identifier):
    pipe = conn.pipeline(True)
    lock_name = 'lock:' + lock_name
    identifier = to_bytes(identifier)

    while True:
        try:
            pipe.watch(lock_name)
            if pipe.get(lock_name) == identifier:
                pipe.multi()
                pipe.delete(lock_name)
                pipe.execute()
                return True

            pipe.unwatch()
            break

        except redis.exceptions.WatchError:
            pass

    return False


def create_user(conn, login, name):
    username = login.lower()

    lock = acquire_lock_with_timeout(conn, 'user:' + username, 1)
    if not lock:
        return None

    if conn.hget('users:', username):
        release_lock(conn, 'user:' + username, lock)
        return None

    uid = conn.incr('user:id:')
    pipeline = conn.pipeline(True)
    pipeline.hset('users:', username, uid)
    pipeline.hset('user:%s' % uid, mapping={
        'login': login,
        'id': uid,
        'name': name,
        'followers': 0,
        'following': 0,
        'posts': 0,
        'signup': time.time(),
    })
    pipeline.execute()
    release_lock(conn, 'user:' + username, lock)
    return uid


def create_status(conn: redis.Redis, uid, message, **data):
    """
    创建一个状态

    :param conn:
    :param uid:
    :param message:
    :param data:
    :return:
    """
    pipeline = conn.pipeline(True)
    pipeline.hget('user:%s' % uid, 'login')
    pipeline.incr('status:id:')
    login, status_id = pipeline.execute()

    print('the status id is:{}, type is: {}'.format(status_id, type(status_id)))

    if not login:
        return None

    data.update({
        'message': message,
        'posted': time.time(),
        'id': status_id,
        'uid': uid,
        'login': login,
    })
    pipeline.hset('status:%s' % status_id, mapping=data)
    pipeline.hincrby('user:%s' % uid, 'posts')
    pipeline.execute()
    return status_id


def get_status_messages(conn, uid, timeline='home:', page=1, count=30):
    """
    获取status 从 homeline

    :param conn:
    :param uid:
    :param timeline:
    :param page:
    :param count:
    :return:
    """
    statuses = conn.zrevrange('%s%s' % (timeline, uid), (page - 1) * count, page * count - 1)

    pipeline = conn.pipeline(True)
    for _id in statuses:
        pipeline.hgetall('status:%s' % (to_str(_id),))

    return [_f for _f in pipeline.execute() if _f]


HOME_TIMELINE_SIZE = 1000


def follow_user(conn: redis.Redis, uid, other_uid):
    fkey1 = 'following:%s' % uid
    fkey2 = 'followers:%s' % other_uid

    # 如果我关注了other,则不用do any action
    if conn.zscore(fkey1, other_uid):
        return None

    now = time.time()

    pipeline = conn.pipeline(True)
    pipeline.zadd(fkey1, {other_uid: now})
    pipeline.zadd(fkey2, {uid: now})
    pipeline.zrevrange('profile:%s' % other_uid, 0, HOME_TIMELINE_SIZE - 1, withscores=True)
    following, followers, status_and_score = pipeline.execute()[-3:]

    pipeline.hincrby('user:%s' % uid, 'following', int(following))
    pipeline.hincrby('user:%s' % other_uid, 'followers', int(followers))
    if status_and_score:
        pipeline.zadd('home:%s' % uid, dict(status_and_score))
    pipeline.zremrangebyrank('home:%s' % uid, 0, -HOME_TIMELINE_SIZE - 1)

    pipeline.execute()
    return True


def unfollow_user(conn, uid, other_uid):
    fkey1 = 'following:%s' % uid
    fkey2 = 'followers:%s' % other_uid

    if not conn.zscore(fkey1, other_uid):
        return None

    pipeline = conn.pipeline(True)
    pipeline.zrem(fkey1, other_uid)
    pipeline.zrem(fkey2, uid)
    pipeline.zrevrange('profile:%s' % other_uid, 0, HOME_TIMELINE_SIZE - 1)
    following, followers, statuses = pipeline.execute()[-3:]

    pipeline.hincrby('user:%s' % uid, 'following', -int(following))
    pipeline.hincrby('user:%s' % other_uid, 'followers', -int(followers))
    if statuses:
        pipeline.zrem('home:%s' % uid, *statuses)

    pipeline.execute()
    return True


def execute_later(conn, queue, name, args):
    # this is just for testing purposes
    assert conn is args[0]
    t = threading.Thread(target=globals()[name], args=tuple(args))
    t.setDaemon(True)
    t.start()


def post_status(conn: redis.Redis, user_id, message, **data):
    status_id = create_status(conn, user_id, message, **data)
    if not status_id:
        return None

    # 获取发布时间
    posted = conn.hget('status:%s' % status_id, 'posted')
    if not posted:
        return None

    post = {str(status_id): float(posted)}
    conn.zadd('profile:%s' % user_id, post)  # 发布状态

    syndicate_status(conn, user_id, post)
    return status_id


POSTS_PER_PASS = 1000


def syndicate_status(conn: redis.Redis, uid, post, start=0):
    # TODO need print
    # 获取关注者列表
    followers = conn.zrangebyscore('followers:%s' % uid, start, 'inf', start=0, num=POSTS_PER_PASS, withscores=True)

    pipeline = conn.pipeline(False)
    for follower, start in followers:  # start 是分值，for 完成之后，会被更新为 最后的分值
        follower = to_str(follower)
        pipeline.zadd('home:%s' % follower, post)  # 给关注者的timeline add post(status_id, time)
        pipeline.zremrangebyrank('home:%s' % follower, 0, -HOME_TIMELINE_SIZE - 1)
    pipeline.execute()

    if len(followers) >= POSTS_PER_PASS:
        execute_later(conn, 'default', 'syndicate_status', [conn, uid, post, start])


def delete_status(conn: redis.Redis, uid, status_id):
    status_id = to_str(status_id)
    key = 'status:%s' % status_id
    lock = acquire_lock_with_timeout(conn, key, 1)
    if not lock:
        return None

    if conn.hget(key, 'uid') != to_bytes(uid):
        release_lock(conn, key, lock)
        return None

    uid = to_str(uid)
    pipeline = conn.pipeline(True)
    pipeline.delete(key)
    pipeline.zrem('profile:%s' % uid, status_id)
    pipeline.zrem('home:%s' % uid, status_id)
    pipeline.hincrby('user:%s' % uid, 'posts', -1)
    pipeline.execute()

    release_lock(conn, key, lock)
    return True


def clean_timelines(conn, uid, status_id, start=0, on_lists=False):
    uid = to_str(uid)
    status_id = to_str(status_id)
    key = 'followers:%s' % uid  # A
    base = 'home:%s'  # A
    if on_lists:  # A
        key = 'list:out:%s' % uid  # A
        base = 'list:statuses:%s'  # A
    followers = conn.zrangebyscore(key, start, 'inf',  # B
                                   start=0, num=POSTS_PER_PASS, withscores=True)  # B

    pipeline = conn.pipeline(False)
    for follower, start in followers:  # C
        follower = to_str(follower)
        pipeline.zrem(base % follower, status_id)  # C
    pipeline.execute()

    if len(followers) >= POSTS_PER_PASS:  # D
        execute_later(conn, 'default', 'clean_timelines',  # D
                      [conn, uid, status_id, start, on_lists])  # D

    elif not on_lists:
        execute_later(conn, 'default', 'clean_timelines',  # E
                      [conn, uid, status_id, 0, True])  # E


if __name__ == '__main__':
    rd = redis.Redis(db=5)

    # create_user(rd, 'user01', 'User 01')
    # create_status(rd, 1, 'xxxxxxxxxxxxxx')
