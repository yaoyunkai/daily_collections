"""
搜索原理

预处理：建索引 反向索引

反向索引会从每个被索引的文档里面提取出一些单词
缩印的结果产生一些单词的集合

语法分析 parsing
标记化 tokenization: 移除内容中非用词 stop word

不同类型的文档都有各自的常用单词，移除非用词的关键就是找到合适的非用词清单

-------------------------------------------------------------
根据多个单词查找文档 --> intersect

多个同义词的单词进行搜索 --> union

包含了特定单词或者锯子，但是并不包含另外一些单词的文档 --> diff


-------------------------------------------------------------

简单地给出单词： inter

某个单词前面有- : all - (-单词) diff

某个单词前面有+ : a +b c     ab 是 union  ab 和 c 是 inter

Create at 2023/3/21 21:16
"""
import re
import uuid

import redis

from generate_document import generate_docs, tokenize as tk

STOP_WORDS = set('''able about across after all almost also am among
an and any are as at be because been but by can cannot could dear did
do does either else ever every for from get got had has have he her
hers him his how however if in into is it its just least let like
likely may me might most must my neither no nor not of off often on
only or other our own rather said say says she should since so some
than that the their them then there these they this tis to too twas us
wants was we were what when where which while who whom why will with
would yet you your'''.split())

WORDS_RE = re.compile(r"[a-z']{2,}")


def tokenize(content):
    words = set()
    for match in WORDS_RE.finditer(content.lower()):
        word = match.group().strip("'")
        if len(word) >= 2:
            words.add(word)
    return words - STOP_WORDS


def index_document(conn, document_id, content, func=tokenize):
    words = func(content)

    pipeline = conn.pipeline(True)
    for word in words:
        pipeline.sadd('idx:' + word, document_id)
    return len(pipeline.execute())


def _set_common(conn: redis.Redis, method, names, ttl=30, execute=True):
    uid = str(uuid.uuid4())
    pipeline = conn.pipeline(True) if execute else conn
    names = ['idx:' + name for name in names]
    getattr(pipeline, method)('idx:' + uid, *names)
    pipeline.expire('idx:' + uid, ttl)
    if execute:
        pipeline.execute()
    return uid


def intersect(conn, items, ttl=30, _execute=True):
    return _set_common(conn, 'sinterstore', items, ttl, _execute)


def union(conn, items, ttl=30, _execute=True):
    return _set_common(conn, 'sunionstore', items, ttl, _execute)


def difference(conn, items, ttl=30, _execute=True):
    return _set_common(conn, 'sdiffstore', items, ttl, _execute)


QUERY_RE = re.compile(r"[+-]?[a-z']{2,}")


def parse(query):
    """
    返回两个变量:

    第一个变量: 一个列表的列表, 内层的同一个列表表示同义词
    第二个变量: 排除列表

    :param query:
    :return:
    """
    # 这个集合将用于储存不需要的单词。
    unwanted_words = set()
    # 这个列表将用于储存需要执行交集计算的单词。
    all_words = []
    # 这个集合将用于储存目前已发现的同义词。
    current_words = set()

    for match in QUERY_RE.finditer(query.lower()):
        word = match.group()
        prefix = word[:1]
        if prefix in '+-':
            word = word[1:]
        else:
            prefix = None

        word = word.strip("'")
        if len(word) < 2 or word in STOP_WORDS:
            continue

        if prefix == '-':
            unwanted_words.add(word)
            continue

        if current_words and not prefix:
            all_words.append(list(current_words))
            current_words = set()
        current_words.add(word)

    if current_words:
        all_words.append(list(current_words))
    return all_words, list(unwanted_words)


def parse_and_search(conn, query, ttl=30):
    all_list, unwanted = parse(query)
    if not all_list:
        return None

    to_intersect = []
    for syn in all_list:
        if len(syn) > 1:
            to_intersect.append(union(conn, syn, ttl=ttl))  # 这里返回一个uid, 也当成一个name返回,实际可能已经获取到结果
        else:
            to_intersect.append(syn[0])  # 每个列表只有一个单词的话，其实不需要搜索

    if len(to_intersect) > 1:
        intersect_result = intersect(conn, to_intersect, ttl=ttl)  # 这里返回一个uid, 也当成一个name返回,实际可能已经获取到结果
    else:
        intersect_result = to_intersect[0]  # 如果列表还是一个单词的话，实际不需要搜索

    if unwanted:
        unwanted.insert(0, intersect_result)  # 这时无论如何 intersect_result都是一个标量值，把它放到第一个，以便进行差集运算
        return difference(conn, unwanted, ttl=ttl)

    return intersect_result  # 最终结果：uid 或者一个单词


"""
排序文章

id: doc08
created: ts
updated: ts
title: xxxx

"""


def search_and_sort(conn, query, uid=None, ttl=300, sort="-updated", start=0, num=20):
    desc = sort.startswith('-')
    sort = sort.lstrip('-')
    by = "doc:*->" + sort  # doc:<id>
    alpha = sort not in ('updated', 'id', 'created')

    if uid and not conn.expire(uid, ttl):
        uid = None

    if not uid:
        uid = parse_and_search(conn, query, ttl=ttl)

    pipeline = conn.pipeline(True)
    pipeline.scard('idx:' + uid)  # doc id numbers
    pipeline.sort('idx:' + uid, by=by, alpha=alpha, desc=desc, start=start, num=num)
    results = pipeline.execute()
    return results[0], results[1], uid


def save_dummy(conn: redis.Redis, numbers=50):
    data_list = generate_docs(numbers)

    for item in data_list:
        content = item.pop('content')
        doc_id = item['id']
        doc_id = 'doc:{}'.format(doc_id)  # doc_id should equal document key
        index_document(conn, doc_id, content, func=tk)
        conn.hset(doc_id, mapping=item)


# =========================================================================

def search_and_zsort(conn: redis.Redis, query, uid=None, ttl=300, update=1, vote=0,
                     start=0, num=20, desc=True):
    if uid and not conn.expire(uid, ttl):
        uid = None

    if not uid:
        uid = parse_and_search(conn, query, ttl=ttl)

        scored_search = {
            uid: 0,
            'sort:update': update,
            'sort:votes': vote
        }
        # for set related, SUM is default aggregate
        uid = zintersect(conn, scored_search, ttl)

    pipeline = conn.pipeline(True)
    pipeline.zcard('idx:' + uid)
    if desc:
        pipeline.zrevrange('idx:' + uid, start, start + num - 1)
    else:
        pipeline.zrange('idx:' + uid, start, start + num - 1)
    results = pipeline.execute()

    return results[0], results[1], uid


def _zset_common(conn, method, scores, ttl=30, **kw):
    uid = str(uuid.uuid4())
    execute = kw.pop('_execute', True)
    pipeline = conn.pipeline(True) if execute else conn
    for key in list(scores.keys()):
        scores['idx:' + key] = scores.pop(key)
    getattr(pipeline, method)('idx:' + uid, scores, **kw)
    pipeline.expire('idx:' + uid, ttl)
    if execute:
        pipeline.execute()
    return uid


def zintersect(conn, items, ttl=30, **kw):
    return _zset_common(conn, 'zinterstore', dict(items), ttl, **kw)


def zunion(conn, items, ttl=30, **kw):
    return _zset_common(conn, 'zunionstore', dict(items), ttl, **kw)


def string_to_score(string, ignore_case=False):
    """
    将字符串转换为分值

    """
    if ignore_case:
        string = string.lower()

    pieces = list(map(ord, string[:6]))
    while len(pieces) < 6:
        pieces.append(-1)

    score = 0
    for piece in pieces:
        score = score * 257 + piece + 1

    return score * 2 + (len(string) > 6)


if __name__ == '__main__':
    rd = redis.Redis(encoding='utf8')

    # save_dummy(rd)
    # ret = search_and_sort(rd, 'relationship +pm')
    # print(ret)

    # print(string_to_score('sdfasfd'))
