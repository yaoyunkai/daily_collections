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
import cgi
import functools
import json
import math
import random
import socket
import socketserver
import threading
import time
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

import faker
import redis

HOME_TIMELINE_SIZE = 1000

POSTS_PER_PASS = 1000


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

    uid = conn.incr('user:id:')  # uid is int
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
    :param uid: must be int or str
    :param message:
    :param data:
    :return: value is int
    """
    pipeline = conn.pipeline(True)
    pipeline.hget('user:%s' % uid, 'login')
    pipeline.incr('status:id:')
    login, status_id = pipeline.execute()

    if not login:
        return None

    data.update({
        'message': message,
        'posted': time.time(),
        'id': status_id,
        'uid': uid,
        'login': to_str(login),
    })
    pipeline.hset('status:%s' % status_id, mapping=data)
    pipeline.hincrby('user:%s' % uid, 'posts')

    # publish
    pipeline.publish('streaming:status:', json.dumps(data))

    pipeline.execute()
    return status_id


def get_status_messages(conn, uid, timeline='home:', page=1, count=30):
    """
    获取status 从 homeline

    :param conn:
    :param uid: must be str or int
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


def follow_user(conn: redis.Redis, uid, other_uid):
    """
    the uid and other_uid should be string

    :param conn:
    :param uid:
    :param other_uid:
    :return:
    """

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
    """
    更新 following followers list

    获取other_id 的posts
    从自己的home line 里面移除 posts

    """

    fkey1 = 'following:%s' % uid
    fkey2 = 'followers:%s' % other_uid

    if not conn.zscore(fkey1, other_uid):
        return None

    pipeline = conn.pipeline(True)
    pipeline.zrem(fkey1, other_uid)  # return is int
    pipeline.zrem(fkey2, uid)
    pipeline.zrevrange('profile:%s' % other_uid, 0, HOME_TIMELINE_SIZE - 1)
    following, followers, statuses = pipeline.execute()[-3:]
    print('unfollow user, posts : {}'.format(statuses))

    pipeline.hincrby('user:%s' % uid, 'following', -int(following))
    pipeline.hincrby('user:%s' % other_uid, 'followers', -int(followers))
    if statuses:
        pipeline.zrem('home:%s' % uid, *statuses)

    pipeline.execute()
    return True


def execute_later(conn, queue, name, args):
    # this is just for testing purposes
    print('the queue is : {}'.format(queue))
    assert conn is args[0]
    t = threading.Thread(target=globals()[name], args=tuple(args))
    """
    在使用 join() 方法时，必须先将守护线程设置为非守护线程（即调用 setDaemon(False) 方法），
    否则会抛出 ValueError 异常。这是因为 join() 方法只能等待非守护线程的结束，而不能等待守护线程的结束。
    """
    t.setDaemon(False)
    t.start()


def post_status(conn: redis.Redis, user_id, message, **data):
    """

    :param conn:
    :param user_id: must be str
    :param message:
    :param data:
    :return:
    """
    status_id = create_status(conn, user_id, message, **data)
    if not status_id:
        return None

    # 获取发布时间
    posted = conn.hget('status:%s' % status_id, 'posted')
    if not posted:
        return None

    post = {str(status_id): float(posted)}
    conn.zadd('profile:%s' % user_id, post)  # 发布状态到自己的homeline

    syndicate_status(conn, user_id, post)  # sync to followers home
    return status_id


def syndicate_status(conn: redis.Redis, uid, post, start=0):
    # 获取关注者列表  (bytes, float)
    followers = conn.zrangebyscore('followers:%s' % uid, start, 'inf', start=0, num=POSTS_PER_PASS, withscores=True)

    pipeline = conn.pipeline(False)
    for follower, start in followers:  # start 是分值，for 完成之后，会被更新为 最后的分值
        follower = to_str(follower)

        # 给关注者的timeline add post(status_id, time)
        # 即使是重复增加post也没有关系, post 不会变多
        pipeline.zadd('home:%s' % follower, post)
        pipeline.zremrangebyrank('home:%s' % follower, 0, -HOME_TIMELINE_SIZE - 1)
    pipeline.execute()

    if len(followers) >= POSTS_PER_PASS:
        execute_later(conn, 'default', syndicate_status.__name__, [conn, uid, post, start])


def delete_status(conn: redis.Redis, uid, status_id):
    """
    uid should be str

    """
    key = 'status:%s' % status_id
    lock = acquire_lock_with_timeout(conn, key, 1)
    if not lock:
        return None

    if conn.hget(key, 'uid') != to_bytes(uid):  # how to support int uid
        release_lock(conn, key, lock)
        return None

    pipeline = conn.pipeline(True)

    # publish
    _status = conn.hgetall(key)
    status = {to_str(k): to_str(v) for k, v in _status.items()}
    status['deleted'] = True
    pipeline.publish('streaming:status:', json.dumps(status))

    pipeline.delete(key)
    pipeline.zrem('profile:%s' % uid, status_id)
    pipeline.zrem('home:%s' % uid, status_id)
    pipeline.hincrby('user:%s' % uid, 'posts', -1)
    pipeline.execute()

    release_lock(conn, key, lock)

    # 会影响到 followers的 home line
    clean_timelines(conn, uid, status_id)
    return True


def clean_timelines(conn, uid, status_id, start=0, on_lists=False):
    if on_lists:
        key = 'list:out:%s' % uid
        base = 'list:statuses:%s'
    else:
        key = 'followers:%s' % uid
        base = 'home:%s'

    followers = conn.zrangebyscore(key, start, 'inf', start=0, num=POSTS_PER_PASS, withscores=True)

    pipeline = conn.pipeline(False)
    for follower, start in followers:
        follower = to_str(follower)
        pipeline.zrem(base % follower, status_id)
    pipeline.execute()

    if len(followers) >= POSTS_PER_PASS:
        execute_later(conn, 'default', 'clean_timelines', [conn, uid, status_id, start, on_lists])

    elif not on_lists:
        execute_later(conn, 'default', 'clean_timelines', [conn, uid, status_id, 0, True])


# -----------------------------------------------------------------------------

def create_dummy_user(numbers=50):
    conn = redis.Redis(db=0)
    _fake = faker.Faker()

    # create dummy user
    username_list = []

    while len(username_list) < numbers:
        un = _fake.user_name()
        if un not in username_list:
            username_list.append(un)

    for username in username_list:
        create_user(conn, username, _fake.name())


def create_dummy_relationship():
    conn = redis.Redis(db=0)

    _all_users = conn.hgetall('users:')
    all_users = {}
    for k, v in _all_users.items():
        all_users[to_str(k)] = to_str(v)
    uid_arr = list(all_users.values())

    for i in range(10):
        uid = random.choice(uid_arr)
        random.shuffle(uid_arr)
        to_flow_arr = uid_arr[:30]

        for to_flow in to_flow_arr:
            follow_user(conn, uid, to_flow)


def post_dummy_posts(numbers=3000):
    _fake = faker.Faker()
    conn = redis.Redis(db=0)

    _all_users = conn.hgetall('users:')
    all_users = {}
    for k, v in _all_users.items():
        all_users[to_str(k)] = to_str(v)
    uid_arr = list(all_users.values())

    for i in range(numbers):
        post_status(conn, random.choice(uid_arr), _fake.sentence())


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

"""
流API需要对外公开哪些事件
是否需要进行访问限制
流API应该提供哪些过滤选项

只要使用chunked传输编码，就可以使用HTTP服务器生成并发送增量式数据
todo: 什么是流式HTTP


"""

CONFIGS = {}
CHECKED = {}
REDIS_CONNECTIONS = {}

# this is a redis Connection
config_connection = None

FILTERS = ('track', 'filter', 'location')


def get_config(conn, _type, component, wait=1):
    key = 'config:%s:%s' % (_type, component)

    if CHECKED.get(key) < time.time() - wait:
        CHECKED[key] = time.time()
        config = json.loads(conn.get(key) or '{}')
        old_config = CONFIGS.get(key)

        if config != old_config:
            CONFIGS[key] = config

    return CONFIGS.get(key)


def redis_connection(component, wait=1):
    key = 'config:redis:' + component

    def wrapper(function):
        @functools.wraps(function)
        def call(*args, **kwargs):
            old_config = CONFIGS.get(key, object())
            _config = get_config(config_connection, 'redis', component, wait)

            config = {}
            for k, v in _config.items():
                config[k.encode('utf-8')] = v

            if config != old_config:
                REDIS_CONNECTIONS[key] = redis.Redis(**config)

            return function(REDIS_CONNECTIONS.get(key), *args, **kwargs)

        return call

    return wrapper


class StreamingAPIServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True


# noinspection PyPep8Naming
class StreamingAPIRequestHandler(BaseHTTPRequestHandler):
    identifier = None
    query = None

    def do_GET(self):
        parse_identifier(self)
        if self.path != '/statuses/sample.json':
            return self.send_error(404)
        process_filters(self)

    def do_POST(self):
        parse_identifier(self)
        if self.path != '/statuses/filter.json':
            return self.send_error(404)
        process_filters(self)


def parse_identifier(handler):
    handler.identifier = None
    handler.query = {}
    if '?' in handler.path:
        handler.path, _, query = handler.path.partition('?')
        handler.query = parse_qs(query)  # query is a dict key:q value is a list
        identifier = handler.query.get('identifier') or [None]
        handler.identifier = identifier[0]


def process_filters(handler):
    ident = handler.identifier
    if not ident:
        return handler.send_error(401, "identifier missing")

    method = handler.path.rsplit('/')[-1].split('.')[0]
    name = None
    args = None
    if method == 'filter':
        data = cgi.FieldStorage(
            fp=handler.rfile,
            headers=handler.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': handler.headers['Content-Type'], })

        for name in data:
            if name in FILTERS:
                args = data.getfirst(name).lower().split(',')
                break

        if not args:
            return handler.send_error(401, "no filter provided")
    else:
        args = handler.query

    handler.send_response(200)
    handler.send_header('Transfer-Encoding', 'chunked')
    handler.end_headers()

    is_quit = [False]
    for item in filter_content(redis.Redis(), ident, method, name, args, is_quit):
        try:
            handler.wfile.write('%X\r\n%s\r\n' % (len(item), item))
        except socket.error:
            is_quit[0] = True
    if not is_quit[0]:
        handler.wfile.write('0\r\n\r\n')


def filter_content(conn, ident, method, name, args, is_quit):
    """
    message type:

    # {'type': 'subscribe', 'pattern': None, 'channel': b'streaming:status:', 'data': 1}
    # {'type': 'message', 'pattern': None, 'channel': b'streaming:status:', 'data': b'qwerqwerqwer'}


    :param conn:
    :param ident:
    :param method:
    :param name:
    :param args:
    :param is_quit:
    :return:
    """
    match = create_filters(ident, method, name, args)

    pubsub = conn.pubsub()
    pubsub.subscribe(['streaming:status:'])

    for item in pubsub.listen():
        message_type = item['type']
        if message_type != 'message':
            continue

        message = item['data']
        decoded = json.loads(message)

        if match(decoded):
            if decoded.get('deleted'):
                yield json.dumps({'id': decoded['id'], 'deleted': True})
            else:
                yield message

        if is_quit[0]:
            break

    pubsub.reset()


def create_filters(ident, method, name, args):
    if method == 'sample':
        return SampleFilter(ident, args)
    elif name == 'track':
        return TrackFilter(args)
    elif name == 'follow':
        return FollowFilter(args)
    elif name == 'location':
        return LocationFilter(args)
    raise Exception("Unknown filter")


def SampleFilter(id, args):  # A
    percent = int(args.get('percent', ['10'])[0], 10)  # B
    ids = list(range(100))  # C
    shuffler = random.Random(id)  # C
    shuffler.shuffle(ids)  # C
    keep = set(ids[:max(percent, 1)])  # D

    def check(status):  # E
        return (status['id'] % 100) in keep  # F

    return check


def TrackFilter(list_of_strings):
    groups = []  # A
    for group in list_of_strings:  # A
        group = set(group.lower().split())  # A
        if group:
            groups.append(group)  # B

    def check(status):
        message_words = set(status['message'].lower().split())  # C
        for group in groups:  # D
            if len(group & message_words) == len(group):  # E
                return True  # E
        return False

    return check


def FollowFilter(names):
    nset = set()  # A
    for name in names:  # B
        nset.add('@' + name.lower().lstrip('@'))  # B

    def check(status):
        message_words = set(status['message'].lower().split())  # C
        message_words.add('@' + status['login'].lower())  # C

        return message_words & nset  # D

    return check


def LocationFilter(list_of_boxes):
    boxes = []  # A
    for start in range(0, len(list_of_boxes) - 3, 4):  # A
        boxes.append(list(map(float, list_of_boxes[start:start + 4])))  # A

    def check(self, status):
        location = status.get('location')  # B
        if not location:  # C
            return False  # C

        lat, lon = list(map(float, location.split(',')))  # D
        for box in self.boxes:  # E
            if (box[1] <= lat <= box[3] and  # F
                    box[0] <= lon <= box[2]):  # F
                return True  # F
        return False

    return check


def start_server():
    server = StreamingAPIServer(('localhost', 8080), StreamingAPIRequestHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()


if __name__ == '__main__':
    rd = redis.Redis()

    # ret = get_status_messages(rd, '20', page=6, count=100)
    # pprint.pprint(ret)

    # start_server()

    post_status(rd, '34', 'this is a text')
