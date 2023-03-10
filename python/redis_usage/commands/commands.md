[TOC]

# Redis comands

当这些命令操作错误的key类型时会报错。

## Strings

### APPEND

```
APPEND key value

return: 追加操作后的字符串长度。

key不存在的话会创建一个新的key
```

### BITCOUNT

```
BITCOUNT key [start end [BYTE | BIT]]

获取string中二进制模式下1的个数。
key不存在不报错，返回0。

start end : 
指出获取string的哪个位置，例如 0 0 就是获取第一个八位的数据，0 1 就是获取第一个和第二个八位的数据。-1 表示最后一个八位。
start end 有点类似闭区间。

127.0.0.1:6379> bitcount k1 0 0
(integer) 3
127.0.0.1:6379> bitcount k1 0 -1
(integer) 30
127.0.0.1:6379> bitcount k1
(integer) 30
127.0.0.1:6379> get k1
"abcabcabc"
```

### BITOP

```
BITOP <AND | OR | XOR | NOT> destkey key [key ...]

在多个键(包含字符串值)之间执行位操作，并将结果存储在目标键中。
return: 存储在目标键中的字符串的大小，等于最长的输入字符串的大小。

127.0.0.1:6379> get k22
"12"   0011000100110010
127.0.0.1:6379> get k33
"45"   0011010000110101
127.0.0.1:6379> bitop AND res k22 k33
(integer) 2
127.0.0.1:6379> get res
"00"   0011000000110000
127.0.0.1:6379>

127.0.0.1:6379> bitop or res1 k22 k33
(integer) 2
127.0.0.1:6379> get res1
"57"   0011010100110111
127.0.0.1:6379>

127.0.0.1:6379> bitop and res2 k22 kndf
(integer) 2
127.0.0.1:6379> get res2
"\x00\x00"  
127.0.0.1:6379>
```

### BITPOS

```
BITPOS key bit [start [end [BYTE | BIT]]]

返回字符串中第一个位设置为1或0的位置。

> bitpos kkkk 0
(integer) 0

> bitpos kkkk 1
(integer) -1

在查找不存在的键时会出现以上结果。我想应该是把不存在的键的value当作全0来操作了。
```

### INCR related

```
decr
incr
decrby
incrby
incrbyfloat

这些命令在操作存在的key时都不会报错，把不存在的key当作0来处理。
但是操作类型不匹配的情况下会报错。

计算的时间以对应类型计算，计算完了将字面量表示转换为二进制存储到数据库中。
```

### GETBIT

```
GETBIT key offset

返回存储在key的字符串值中偏移处的位值。

offset: 0表示第一位 不支持负一，使用-1时会报错，那么取最后一位可以使用 strlen * 8 - 1

```

### GETRANGE

```
GETRANGE key start end

返回存储在key处的字符串值的子字符串，由偏移量start和end决定(两者都包含在内)。
可以使用负偏移量来提供从字符串末尾开始的偏移量。
start end 表示的是一个个字节。
获取不存在的key不会报错，返回""


127.0.0.1:6379> get k2
"-3.14000000000000012"
127.0.0.1:6379> getrange k2 0 -1
"-3.14000000000000012"
127.0.0.1:6379> getrange k2 0 0
"-"
127.0.0.1:6379> getrange k2 0 1
"-3"
127.0.0.1:6379> getrange k2 0 3
"-3.1"
127.0.0.1:6379> getrange k2 0 4
"-3.14"
127.0.0.1:6379> getrange k2 0 5
"-3.140"
127.0.0.1:6379>
```

### GETSET(已弃用)

设置键的字符串值并返回其旧值

return: the old value stored at `key`, or `nil` when `key` did not exist.

### GET / SET related

```
GET key

MGET key [key ...]

MSET key value [key value ...]

MSETNX key value [key value ...]  
将给定的键设置为它们各自的值。即使只有一个键已经存在，MSETNX也不会执行任何操作。
return: 1 表示所有key都已经设置成功，0表示所有键都没有设置

PSETEX key milliseconds value
设置密钥的值和过期时间(以毫秒为单位)

SET key value [expiration EX seconds|PX milliseconds] [NX|XX]
设置key保存字符串值。如果key已经保存了一个值，那么无论它的类型是什么，它都将被覆盖。
在成功的SET操作时，将丢弃与该键关联的任何先前存活时间。
EX: 过期时间 second
PX: 过期时间 milliseconds
NX -- 仅在该键不存在时设置该键。
XX -- 只在已经存在的情况下设置键。
由于SET命令选项可以替代SETNX, SETEX, PSETEX, GETSET，在Redis的未来版本中，这些命令可能会被弃用并最终删除。
return: simple OK / NULL 如果由于用户指定了NX或XX选项但条件不满足而没有执行SET操作。

```

### SETBIT

```
SETBIT key offset value
设置或清除存储在key上的字符串偏移位的值
return: 返回该位置上原来的位的值。

127.0.0.1:6379> setbit k324123  0 1
(integer) 0
127.0.0.1:6379> setbit k324123  0 0
(integer) 1
127.0.0.1:6379> setbit k324123  0 1
(integer) 0
127.0.0.1:6379> setbit k324123  0 0
(integer) 1
```

### SETRANGE

```
SETRANGE key offset value
覆盖存储在key上的字符串的一部分，从指定的偏移量开始，覆盖value的整个长度。

return:字符串被命令修改后的长度。

127.0.0.1:6379> get k4
"4555"
127.0.0.1:6379> setrange k4 0 5
(integer) 4
127.0.0.1:6379> get k4
"5555"
127.0.0.1:6379> setrange k4 2 66
(integer) 4
127.0.0.1:6379> get k4
"5566"
127.0.0.1:6379> setrange k4 3 7
(integer) 4
127.0.0.1:6379> get k4
"5567"
127.0.0.1:6379> setrange k4 4 8888
(integer) 8
127.0.0.1:6379> get k4
"55678888"
127.0.0.1:6379>
```

### SRTLEN

获取存储在键中的值的长度,不存在的key返回0

## List

当list中的value被remove all时，key会被删除。

### BLPOP / BRPOP

```
BLPOP key [key ...] timeout

BLPOP是一个阻塞列表流行原语。它是LPOP的阻塞版本，因为当任何给定的列表中都没有弹出元素时，它会阻塞连接。
如果给定的键有一个是非空队列，那么就会从队列中弹出队列头部的值。

非阻塞行为: BLPOP保证从存储在list2的列表中返回一个元素(因为在按顺序检查list1、list2和list3时，它是第一个非空列表)。

阻塞行为: 当BLPOP导致客户端阻塞并且指定了非零超时时，当指定的超时已过期时，客户端将取消阻塞，返回一个空的多批量值，而不对至少一个指定的键进行推操作。

在MULTI/EXEC内部的表现: 没有多大意义。

return: null如果超时，返回一个(key, value)的tuple


127.0.0.1:6379> blpop arr1 arr2 5
1) "arr1"
2) "e"
```

### RPOPLPUSH / BRPOPLPUSH

```
RPOPLPUSH source destination
原子地返回并删除存储在源列表中的最后一个元素(尾部)，并将元素推入存储在目标列表中的第一个元素(头部)。
如果source不存在，则返回值为nil，不执行任何操作。
如果源和目标相同，该操作相当于从列表中删除最后一个元素，并将其作为列表的第一个元素推入，因此可以将其视为一个列表旋转命令。

return: 源不存在返回null，存在则返回被移除的元素。

BRPOPLPUSH source destination timeout
BRPOPLPUSH是RPOPLPUSH的阻塞变体。
当source包含元素时，此命令的行为与RPOPLPUSH完全相同。
当在MULTI/EXEC块中使用时，此命令的行为与RPOPLPUSH完全相同。
当source为空时，Redis将阻塞连接，直到另一个客户端推送到它或直到超时。0的超时可以用来无限期地阻塞。

127.0.0.1:6379> LLEN arr1
(integer) 4
127.0.0.1:6379> rpoplpush arr2 arr1
(nil)
127.0.0.1:6379> rpoplpush arr1 arr2
"a"
127.0.0.1:6379> rpoplpush arr1 arr2
"b"
127.0.0.1:6379> rpoplpush arr1 arr2
"c"
127.0.0.1:6379> rpoplpush arr1 arr2
"d"
127.0.0.1:6379> rpoplpush arr1 arr2
(nil)
127.0.0.1:6379> rpoplpush arr1 arr2
(nil)
127.0.0.1:6379>
```

### LINDEX

```
LINDEX key index

127.0.0.1:6379> lindex ndf 0
(nil)
127.0.0.1:6379> lindex ndf 1
(nil)
127.0.0.1:6379> lindex arr2 0
"d"
127.0.0.1:6379> lindex arr2 5
(nil)
127.0.0.1:6379>
```

### LINSERT

```
LINSERT key <BEFORE | AFTER> pivot element

pivot是该列表中的某个元素
如果key不存在那么不会有key被添加，此时返回0
如果pivot没找到元素，那么返回-1
如果成功找到pivot并插入元素，那么返回list的长度

127.0.0.1:6379> LRANGE arr2 0 -1
1) "d"
2) "c"
3) "b"
4) "a"
127.0.0.1:6379> LINSERT arr2 after c 123w
(integer) 5
127.0.0.1:6379> LRANGE arr2 0 -1
1) "d"
2) "c"
3) "123w"
4) "b"
5) "a"
127.0.0.1:6379> LINSERT arr21 after c 123w
(integer) 0
127.0.0.1:6379> lrange arr21 0 -1
(empty list or set)
127.0.0.1:6379>
```

### LLEN

```
llen key 
获取某个key的长度

```

### LPOP / RPOP

```
LPOP key [count]

6.2.0 add count argument
删除并返回存储在key的列表的第一个元素。

127.0.0.1:6379> LRANGE arr2 0 -1
1) "d"
2) "c"
3) "123w"
4) "b"
5) "a"
127.0.0.1:6379> lpop arr2 3
(error) ERR wrong number of arguments for 'lpop' command
127.0.0.1:6379> lpop arr2
"d"
127.0.0.1:6379> lpop arr2
"c"
127.0.0.1:6379> lpop ndf
(nil)
127.0.0.1:6379> lpop arr2
"123w"
127.0.0.1:6379> lpop arr2
"b"
127.0.0.1:6379> lpop arr2
"a"
127.0.0.1:6379> lpop arr2
(nil)
127.0.0.1:6379> lpop arr2
(nil)
127.0.0.1:6379>
```

### LPUSH / RPUSH

```
LPUSH key element [element ...]

return: 推入操作后的列表长度。

```

### LPUSHX / RPUSHX

```
LPUSHX key element [element ...]

仅当key已存在并保存列表时，才在存储在key的列表头部插入指定值。
与LPUSH相反，当key不存在时，将不执行任何操作。
return: 推入操作后的列表长度。
```

### LRANGE

```
LRANGE key start stop

返回列表中存储在key的指定元素。偏移量开始和停止是从零开始的索引，0是列表的第一个元素(列表的头)，1是下一个元素，依此类推。

超出范围的索引不会产生错误。如果start大于列表的结束，则返回空列表。如果stop大于列表的实际结束，Redis会将其视为列表的最后一个元素。

```

### LREM

```
LREM key count element
count:
	等于0， 移除所有与element相等的元素
	小于0， 移除从尾到头 count个与element相等的元素
	大于0， 移除从头到尾 count个与element相等的元素
return: 移除的元素的个数


127.0.0.1:6379> lrange arr1 0 -1
1) "444"
2) "b"
3) "bb"
127.0.0.1:6379> lpush arr1 b
(integer) 4
127.0.0.1:6379> rpush arr1 b
(integer) 5
127.0.0.1:6379> lrange arr1 0 -1
1) "b"
2) "444"
3) "b"
4) "bb"
5) "b"
127.0.0.1:6379> lrem arr1 -1 b
(integer) 1
127.0.0.1:6379> lrange arr1 0 -1
1) "b"
2) "444"
3) "b"
4) "bb"
127.0.0.1:6379> lrem arr1 1 b
(integer) 1
127.0.0.1:6379> lrange arr1 0 -1
1) "444"
2) "b"
3) "bb"
127.0.0.1:6379>
```

### LSET

```
LSET key index element
return: simple return if OK, else raise error if out of range

127.0.0.1:6379> lrange arr1 0 -1
1) "444"
2) "b"
3) "bb"
127.0.0.1:6379> lset arr1 0 333
OK
127.0.0.1:6379> lrange arr1 0 -1
1) "333"
2) "b"
3) "bb"
127.0.0.1:6379> lset arr1 -1 666
OK
127.0.0.1:6379> lrange arr1 0 -1
1) "333"
2) "b"
3) "666"
127.0.0.1:6379> lset arr1 5 456
(error) ERR index out of range
127.0.0.1:6379>
```

### LTRIM

```
LTRIM key start stop
修剪现有列表，使其仅包含指定元素的指定范围。

127.0.0.1:6379> ltrim arr1 0 -2  # 移除最后一个元素
OK
127.0.0.1:6379> lrange arr1 0 -1
1) "333"
2) "b"
127.0.0.1:6379>
```

## Set

对应于python的set

```
读取相关
SCARD   获取元素数量
SIIMEMBER  元素是否在key
SMEMBERS   获取所有元素
SRANDMEMBER key [count]  随机获取count个元素  
SSCAN

增加/移除
SADD key member [member ...]  新增元素
SMOVE source destination member:  Move a member from one set to another
SPOP key [count]   
SREM key member [member ...]  

集合操作
SDIFF           差集
SDIFFSTORE
SINTER          交集
SINTERSTORE
SUNION          并集
SUNIONSTORE


127.0.0.1:6379> SMEMBERS s1
1) "a"
2) "c"
3) "b"
4) "d"
127.0.0.1:6379> SMEMBERS s2
1) "f"
2) "c"
3) "e"
4) "d"
127.0.0.1:6379> SINTER s1 s2
1) "c"
2) "d"
127.0.0.1:6379> SINTER s2 s1
1) "c"
2) "d"
127.0.0.1:6379> SDIFF s1 s2
1) "a"
2) "b"
127.0.0.1:6379> SDIFF s2 s1
1) "f"
2) "e"
127.0.0.1:6379> SUNION s1 s2
1) "d"
2) "a"
3) "f"
4) "c"
5) "b"
6) "e"
```

### SSCAN

关于SSCAN的用法：

与之相关的命令有: `SCAN` `HSCAN` `SSCAN` `ZSCAN`

[SCAN | Redis](https://redis.io/commands/scan/)

```
SSCAN key cursor [MATCH pattern] [COUNT count]

cursor: 默认都是以0开始
pattern: 指出要匹配的元素的模式
count: 指出要匹配的元素的数量

127.0.0.1:6379> sscan s1 0 match a* count 3
1) "6"
2) 1) "a"
   2) "abr"
   3) "aa"
127.0.0.1:6379> sscan s1 6 match a* count 3
1) "3"
2) 1) "aa3"
   2) "aa2"
   3) "absdf"
   4) "abd"
127.0.0.1:6379> sscan s1 3 match a* count 3
1) "7"
2) 1) "aa1"
   2) "abc"
127.0.0.1:6379> sscan s1 7 match a* count 3
1) "0"     最后会以0结束
2) (empty list or set)
```

## Hash

对应于python的字典

```
读取相关
HEXISTS key field
HGET key field
HGETALL key
HKEYS key 获取字典中所有的key
HVALS key 获取字典中所有的value
HLEN key 获取字典中元素的个数
HMGET key field [field ...]
HSCAN key cursor [MATCH pattern] [COUNT count]
HSTRLEN key field   获取给定字段

增加相关
HINCRBY key field increment
HINCRBYFLOAT key field increment
HMSET key field value [field value ...]
HSET key field value
HSETNX key field value     仅当哈希字段不存在时，才设置该字段的值


删除相关
HDEL key field [field ...]   删除字典中的键

```

## Sorted Set

有序集合：不会有相同的成员member，但是会有相同的分数score

分数越小，越靠近头部。

```

### 都是获取元素，只是条件不一样。
ZRANGE key start stop [WITHSCORES]
ZRANGEBYLEX key min max [LIMIT offset count]
ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]
ZREVRANGE key start stop [WITHSCORES]
ZREVRANGEBYLEX key max min [LIMIT offset count]
ZREVRANGEBYSCORE key max min [WITHSCORES] [LIMIT offset count]



BZPOPMAX key [key ...] timeout
BZPOPMIN key [key ...] timeout
ZPOPMAX key [count]
ZPOPMIN key [count]

ZREM key member [member ...]
ZREMRANGEBYLEX key min max
ZREMRANGEBYRANK key start stop
ZREMRANGEBYSCORE key min max


ZADD key [NX|XX] [CH] [INCR] score member [score member ...]
ZINCRBY key increment member


ZINTERSTORE destination numkeys key [key ...] [WEIGHTS weight] [AGGREGATE SUM|MIN|MAX]
ZUNIONSTORE destination numkeys key [key ...] [WEIGHTS weight] [AGGREGATE SUM|MIN|MAX]

```

### 获取信息，返回标量

```
ZCARD key    返回元素的数量
ZCOUNT key min max   根据分数区间统计元素个数
ZLEXCOUNT key min max
ZSCORE key member     获取元素的分数，不存在则返回null
ZRANK key member        返回元素的排序，从下标0开始，如果元素不存在则返回null
ZREVRANK key member     返回元素的反向排序，从下标0开始，如果元素不存在则返回null

ZSCAN key cursor [MATCH pattern] [COUNT count]
```

