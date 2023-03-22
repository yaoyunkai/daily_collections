"""

布隆过滤器（Bloom Filter）是一种用于快速判断一个元素是否属于某个集合的数据结构。
它可以在常数时间内判断某个元素是否可能在集合中，但也可能会误判一些不在集合中的元素。
这种误判的概率是可以被控制的，并且与布隆过滤器的容量和集合中元素的数量有关。


布隆过滤器的核心是一个二进制向量和一组哈希函数。
在添加元素时，哈希函数会将元素映射到二进制向量的若干个位置上，并将这些位置的值设置为1。
在查询元素时，哈希函数会再次将元素映射到二进制向量的若干个位置上，并检查这些位置的值是否都为1。
如果所有位置的值都为1，那么就认为元素可能在集合中；如果有任何一个位置的值为0，那么就认为元素一定不在集合中。


Created at 2023/3/22
"""

import hashlib
import math

import mmh3
import redis


def get_hash(item, index):
    hash_func = hashlib.sha256()
    hash_func.update(str(index).encode('utf-8'))
    hash_func.update(str(item).encode('utf-8'))
    return int(hash_func.hexdigest(), 16)


class BloomFilter(object):
    def __init__(self, capacity, error_rate):
        self.capacity = capacity
        self.error_rate = error_rate
        self.bit_array_size = self._get_bit_array_size()
        self.num_hashes = self._get_num_hashes()
        self.redis_conn = redis.Redis(host='localhost', port=6379, db=0)

    def _get_bit_array_size(self):
        bit_array_size = int(math.ceil(self.capacity * abs(math.log(self.error_rate)) / (math.log(2) ** 2)))
        return bit_array_size

    def _get_num_hashes(self):
        num_hashes = int(round((self.bit_array_size / self.capacity) * math.log(2)))
        return num_hashes

    def add(self, item):
        for i in range(self.num_hashes):
            index = get_hash(item, i) % self.bit_array_size
            self.redis_conn.setbit("bloomfilter", index, 1)

    def contains(self, item):
        for i in range(self.num_hashes):
            index = get_hash(item, i) % self.bit_array_size
            if not self.redis_conn.getbit("bloomfilter", index):
                return False
        return True


class BloomFilter2:
    def __init__(self, capacity, error_rate):
        self.redis_client = redis.StrictRedis()
        self.bit_size = self.get_bit_size(capacity, error_rate)
        self.hash_count = self.get_hash_count(self.bit_size, capacity)
        self.key = 'bloomfilter'
        self.init_bloomfilter()

    def get_bit_size(self, capacity, error_rate):
        m = -1 * capacity * math.log(error_rate) / math.log(2) ** 2
        return int(m)

    def get_hash_count(self, bit_size, capacity):
        k = bit_size / capacity * math.log(2)
        return int(k)

    def init_bloomfilter(self):
        if not self.redis_client.exists(self.key):
            self.redis_client.setbit(self.key, self.bit_size - 1, 0)

    def add(self, value):
        for i in range(self.hash_count):
            index = mmh3.hash(value, i) % self.bit_size
            self.redis_client.setbit(self.key, index, 1)

    def exists(self, value):
        for i in range(self.hash_count):
            index = mmh3.hash(value, i) % self.bit_size
            if self.redis_client.getbit(self.key, index) == 0:
                return False
        return True
