"""

GoldBoard

怎样阻止用户拿到Conn删除redis数据????
post到远程的API


数据结构:

goldboard                  hash   gb:object:<sernum>
goldboard list             zset   gb:list               member: gb:object:<sernum>


Created at 2023/3/18
"""

import pickle
import time

import redis

ENCODING = 'utf8'


def _dump_data(val: dict):
    if not isinstance(val, dict):
        raise TypeError('the data must be dict')
    try:
        return pickle.dumps(val, protocol=pickle.DEFAULT_PROTOCOL)
    except Exception as e:
        raise ValueError('the value can\'t serialize: {}'.format(e))


def _dump_blank():
    return pickle.dumps({}, protocol=pickle.DEFAULT_PROTOCOL)


def _load_data(val: bytes):
    try:
        return pickle.loads(val)
    except Exception as e:
        print(e)
        return {}


def _parse_gb_object_from_db(val: dict):
    _new_dict = {}

    for k, v in val.items():
        k = k.decode(ENCODING)

        if k == 'user_parameters':
            v = _load_data(v)
        else:
            v = v.decode(ENCODING)

        _new_dict[k] = v

    return _new_dict


def get_goldboard(conn: redis.Redis, serial_number, timeout=5):
    """
    serial_number: str
    user_parameters: dict

    """
    gb_key = 'gb:object:{}'.format(serial_number)
    gb_list_key = 'gb:list'

    pipe = conn.pipeline()

    end_time = time.time() + timeout

    while time.time() < end_time:
        try:
            pipe.watch(gb_list_key)
            exists = pipe.zscore(gb_list_key, gb_key)
            pipe.multi()
            if not exists:
                _data = {
                    'serial_number': serial_number,
                    'user_parameters': _dump_blank(),
                }

                pipe.zadd(gb_list_key, {gb_key: time.time()})
                pipe.hset(gb_key, mapping=_data)

            else:
                pipe.unwatch()

            pipe.hgetall(gb_key)
            _data = pipe.execute()[-1]
            return _parse_gb_object_from_db(_data)

        except redis.exceptions.WatchError:
            continue

    return None


def update_user_parameters(conn: redis.Redis, sernum, new_data: dict):
    gb_key = 'gb:object:{}'.format(sernum)
    gb_list_key = 'gb:list'

    exists = conn.zscore(gb_list_key, gb_key)
    if not exists:
        return False
    new_data = _dump_data(new_data)
    conn.hset(gb_key, 'user_parameters', new_data)
    return True
