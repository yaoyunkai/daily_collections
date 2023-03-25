"""
Redis事务问题

在 Redis 中，事务（Transaction）是一组命令的有序集合，由 MULTI 和 EXEC 命令标记起始和结束位置。
在一个事务中，所有的命令都会被序列化，并在 EXEC 命令执行时一次性被执行。
因此，在一个客户端执行事务期间，其他客户端仍然可以执行命令。

在执行事务期间，其他客户端的命令将被正常执行，并将被立即执行，而不会等待事务执行完成。
但是，其他客户端执行的命令会在事务提交前或回滚后立即生效，这可能会对事务的结果产生影响。

需要注意的是，事务期间的所有操作都是原子性的，意味着在事务执行期间，其他客户端对执行事务的客户端的操作是不可见的。

数据结构:
    1. 用户信息   hash  key  users:<user_id>
    2. 用户包裹   set   key  inventory:<user_id>
    3. 市场      zset  key  market:    member:   <goods>.<owner_user_id>



Create at 2023/3/14 21:36
"""
import time

import redis


def list_item(conn: redis.Redis, item_id, seller_id, price):
    inventory = 'inventory:{}'.format(seller_id)
    item = '{}.{}'.format(item_id, seller_id)

    end_time = time.time() + 5
    pipe = conn.pipeline()

    while time.time() < end_time:
        try:  # 重试上架动作
            pipe.watch(inventory)  # watch 一个 key
            if not pipe.sismember(inventory, item_id):
                pipe.unwatch()  # 不存在 unwatch 一个 key
                return None

            pipe.multi()  # 开启事务
            pipe.zadd('market:', {item: price})
            pipe.srem(inventory, item_id)
            pipe.execute()  # 从multi到exec的命令将会一起执行
            return True  # 没有发生 WatchError 说明key没有被更改，监视完成

        except redis.exceptions.WatchError:
            pass

    return False


def purchase_item(conn: redis.Redis, buyer_id, item_id, seller_id, lprice):
    buyer = "users:%s" % buyer_id
    seller = "users:%s" % seller_id
    item = "%s.%s" % (item_id, seller_id)
    inventory = "inventory:%s" % buyer_id
    end = time.time() + 10
    pipe = conn.pipeline()

    while time.time() < end:
        try:
            pipe.watch('market:', buyer)  # 监视 市场和买家

            price = pipe.zscore("market:", item)
            funds = int(pipe.hget(buyer, "funds"))
            if price != lprice or price > funds:
                pipe.unwatch()
                return None

            pipe.multi()
            pipe.hincrby(seller, "funds", int(price))  # 给卖家增加
            pipe.hincrby(buyer, "funds", int(-price))  # 给买家减少
            pipe.sadd(inventory, item_id)  # 将商品加入到买家的包裹
            pipe.zrem("market:", item)  # 从市场溢出商品
            pipe.execute()
            return True

        except redis.exceptions.WatchError:
            pass

    return False


def update_token(conn, token, user, item=None):
    timestamp = time.time()
    conn.hset('login:', token, user)
    conn.zadd('recent:', {token: timestamp})
    if item:
        conn.zadd('viewed:' + token, {item: timestamp})
        conn.zremrangebyrank('viewed:' + token, 0, -26)
        conn.zincrby('viewed:', -1, item)


def update_token_pipeline(conn, token, user, item=None):
    """
    即使在非事务型流水线中, 也不会立即执行命令
    pipeline_execute_command return的是 Pipe Object, 所以不能获取命令执行结果

    :param conn:
    :param token:
    :param user:
    :param item:
    :return:
    """
    timestamp = time.time()
    pipe = conn.pipeline(False)
    pipe.hset('login:', token, user)
    pipe.zadd('recent:', {token: timestamp})
    if item:
        pipe.zadd('viewed:' + token, {item: timestamp})
        pipe.zremrangebyrank('viewed:' + token, 0, -26)
        pipe.zincrby('viewed:', -1, item)
    pipe.execute()


if __name__ == '__main__':
    rd = redis.Redis()
    update_token_pipeline(rd, '12345', '3333', 'post')
