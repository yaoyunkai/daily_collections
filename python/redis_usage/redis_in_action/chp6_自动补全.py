"""

自动补全

数据结构
列表


Create at 2023/3/20 21:21
"""
import bisect
import uuid

import faker
import redis


def add_update_contact(conn: redis.Redis, user, contact):
    ac_list = 'recent:{}'.format(user)
    pipe = conn.pipeline(True)
    # count: 0 remove all
    pipe.lrem(ac_list, 0, contact)
    pipe.lpush(ac_list, contact)
    pipe.ltrim(ac_list, 0, 99)
    pipe.execute()


def remove_contact(conn: redis.Redis, user, contact):
    conn.lrem('recent:{}'.format(user), 0, contact)


def fetch_autocomplete_list(conn: redis.Redis, user, prefix):
    candidates = conn.lrange('recent:{}'.format(user), 0, -1)
    matches = []

    for item in candidates:
        item = item.decode('utf8')
        if item.lower().startswith(prefix):
            matches.append(item)

    return matches


# =============================================================================

"""
使用zset

查找abc前缀的单词，实际上是查找 abbz ~ zbd 之间的字符串，如果我们知道第一个排在abbz之前的元素的排名
和第一个排在abd之后的元素排名

先将这两个元素插入到zset，接着根据这两个元素的排名来调用zrange

在ASCII码中 `在a之前， {在z之后。

将{拼接到abc abc{   ----> 这个元素位于abd之前，又位于所有带有abc前缀的合法名字之后

将{追加到 abb的末尾     abb{   ---->  这个元素位于所有带有abc前缀的合法名字之前

当查找前缀aba时，可以使用 ab` 作为起始元素 aba{ 作为结束元素

todo 应该是可以使用 zrangebylex 


"""

valid_characters = '`abcdefghijklmnopqrstuvwxyz{'


def find_prefix_range(prefix):
    # 在字符列表中查找前缀字符所处的位置。
    posn = bisect.bisect_left(valid_characters, prefix[-1:])
    # 找到前驱字符。
    suffix = valid_characters[(posn or 1) - 1]
    # 返回范围。
    return prefix[:-1] + suffix + '{', prefix + '{'


def autocomplete_on_prefix(conn: redis.Redis, guild, prefix):
    start, end = find_prefix_range(prefix)
    identifier = str(uuid.uuid4())
    start += identifier
    end += identifier
    zset_name = 'members:' + guild

    items = []

    conn.zadd(zset_name, {start: 0, end: 0})
    pipeline = conn.pipeline(True)
    while 1:
        try:
            pipeline.watch(zset_name)
            start_index = pipeline.zrank(zset_name, start)
            end_index = pipeline.zrank(zset_name, end)
            end_range = min(start_index + 9, end_index - 2)
            pipeline.multi()
            pipeline.zrem(zset_name, start, end)
            pipeline.zrange(zset_name, start_index, end_range)
            items = pipeline.execute()[-1]
            break
        except redis.exceptions.WatchError:
            continue

    return [item.decode('utf8') for item in items if b'{' not in item]


def join_guild(conn: redis.Redis, guild, user):
    conn.zadd('members:' + guild, {user: 0})


def leave_guild(conn, guild, user):
    conn.zrem('members:' + guild, user)


if __name__ == '__main__':
    rd = redis.Redis()
    fk = faker.Faker()

    # for i in range(100):
    #     join_guild(rd, 'group2', fk.name().lower())

    # ret = fetch_autocomplete_list(rd, 'user1', 'de')
    # print(ret)

    # print(find_prefix_range('abc'))

    print(autocomplete_on_prefix(rd, 'group2', 'z'))
