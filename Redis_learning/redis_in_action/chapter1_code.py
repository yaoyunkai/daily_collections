"""
第一章示例程序

随着时间流逝不断减少的评分: 程序需要根据文章的发布时间和当前时间来计算文章评分

数据结构:
    1. 文章 hash                   key article:<article_id>
    2. 文章的发布时间: zset          key time:
    3. 文章的评分: zset             key score:
    4. 每篇文章已投票的用户名单: set   key voted:<article_id>
    5. 文章分组 set                 key  groups:<group_name>


Create at 2023/3/12 20:55
"""
import time

import redis

VOTE_SCORE = 432  # 假设有趣的文章需要200票, 将一天的秒数除以文章展示一天所需的支持票 86400 / 200
ONE_WEEK_IN_SECONDS = 7 * 86400
ARTICLES_PER_PAGE = 25


def article_vote(conn: redis.Redis, user: str, article: str):
    """
    给文章投票


    :param conn: Redis Connection
    :param user:   user:<id>
    :param article: article:<id>
    :return:
    """

    cutoff = time.time() - ONE_WEEK_IN_SECONDS
    if conn.zscore('time:', article) < cutoff:  # python will convert result to null / float
        print('投票时间已过...')
        return

    article_id = article.partition(':')[-1]
    key_voted_set = 'voted:{}'.format(article_id)
    if conn.sadd(key_voted_set, user):  # result is int
        conn.zincrby('score:', VOTE_SCORE, article)  # result is float / null
        conn.hincrby(article, 'votes', 1)


def post_article(conn: redis.Redis, user, title, link):
    article_id = str(conn.incr('article:'))  # return int

    voted = 'voted:' + article_id
    conn.sadd(voted, user)  # 创建一个已投票名单，默认自己给自己的文章投一票
    conn.expire(voted, ONE_WEEK_IN_SECONDS)  # 一周后过期

    now = time.time()
    article = 'article:' + article_id
    conn.hset(article, mapping={
        'title': title,
        'link': link,
        'poster': user,
        'time': now,
        'votes': 1,
    })
    conn.zadd('score:', {article: now + VOTE_SCORE})  # 创建分数表
    conn.zadd('time:', {article: now})  # 创建文章时间表

    return article_id


def get_articles(conn: redis.Redis, page, order='score:'):
    """
    按照评分获取文章

    :param conn:
    :param page:
    :param order:
    :return:
    """
    start = (page - 1) * ARTICLES_PER_PAGE
    end = start + ARTICLES_PER_PAGE - 1  # redis命令的范围是闭区间
    ids = conn.zrevrange(order, start, end, )  # return list[members] or list[(member: bytes, score: float)]
    articles = []

    for idx in ids:
        article_data = conn.hgetall(idx)  # key value is bytes
        article_data[b'id'] = idx
        articles.append(article_data)

    return articles


def add_remove_groups(conn: redis.Redis, article_id, to_add=None, to_remove=None):
    """
    给文章添加或者移除分组

    :param conn:
    :param article_id:
    :param to_add:
    :param to_remove:
    :return:
    """
    article = 'article:' + article_id

    if type(to_add) is not list:
        to_add = []
    if type(to_remove) is not list:
        to_remove = []

    for group in to_add:
        conn.sadd('group:' + group, article)  # result is int
    for group in to_remove:
        conn.srem('group:' + group, article)  # result is int


def get_group_articles(conn: redis.Redis, group, page, order='score:'):
    """
    获取分组的文章

    :param conn:
    :param group:
    :param page:
    :param order:
    :return:
    """
    key = 'cache:' + order + group
    if not conn.exists(key):
        conn.zinterstore(key, ['group:' + group, order], aggregate='max')
        conn.expire(key, 600)
    return get_articles(conn, page, key)


if __name__ == '__main__':
    rd = redis.Redis()
    # post_article(rd, 'user:123', 'this is a article 111111111', 'this is a link for post')
    # post_article(rd, 'user:124', 'this is a article xxxxxxxxxxxx', 'this is a link for post')
    # post_article(rd, 'user:125', 'this is a article 33333333333', 'this is a link for post')
    # post_article(rd, 'user:126', 'this is a article 55555555555555', 'this is a link for post')

    # article_vote(rd, 'user:444', 'article:2')
    # article_vote(rd, 'user:456', 'article:2')
    # article_vote(rd, 'user:45', 'article:2')
    # article_vote(rd, 'user:55', 'article:2')
    # article_vote(rd, 'user:56', 'article:2')
    # article_vote(rd, 'user:57', 'article:2')
    # article_vote(rd, 'user:58', 'article:2')
    # article_vote(rd, 'user:59', 'article:2')
    # article_vote(rd, 'user:69', 'article:2')
    # article_vote(rd, 'user:44', 'article:2')
    # article_vote(rd, 'user:56', 'article:2')

    # print(rd.zrevrange('score:', 0, -1, withscores=True))
    # print(rd.zrevrange('score:', 0, -1, withscores=False))

    # print(get_articles(rd, 1))
