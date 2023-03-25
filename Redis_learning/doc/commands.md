[TOC]

# Redis comands

当这些命令操作错误的key类型时会报错。

## Generic

### DEL

```
DEL key [key ...]
```

### DUMP / RESTORE

```
DUMP key
序列化key的内容

127.0.0.1:6379> dump s3
"\x0c33\x00\x00\x00/\x00\x00\x00\x0e\x00\x00\x01a\x03\xfc\x02\x01b\x03\xfd\x02\x01c\x03\xfe\r\x03\x01f\x03\xfe\x0e\x03\x01g\x03\xfe\x10\x03\x01h\x03\xfe\x12\x03\x01d\x03\xfe\x1a\xff\t\x00O\x9ew\xf8\xc8\x0b\x83+"

RESTORE key ttl serialized-value [REPLACE] [ABSTTL] [IDLETIME seconds] [FREQ frequency]

```

### EXISTS

```
EXISTS key [key ...]
判断一个key是否存在

```

### 键过期时间

| 命令        | 描述                         |
|-----------|----------------------------|
| PERSIST   | 移除键的过期时间                   |
| TTL       | 查看键距离过期还有多少秒               |
| EXPIRE    | 给键指定过期时间(秒)                |
| EXPIREAT  | 将给定键的过期时间设置为给定unix时间戳      |
| PTTL      | 距离过期时间还有多少毫秒               |
| PEXPIRE   | 给键指定过期的毫秒数                 |
| PEXPIREAT | 将一个毫秒精度的unix时间戳设置为给定键的过期时间 |

```
127.0.0.1:6379> ttl s3
(integer) -1
127.0.0.1:6379> ttl s3
(integer) -1
127.0.0.1:6379> PEXPIRE s3 600000
(integer) 1
127.0.0.1:6379> ttl s3
(integer) 595
127.0.0.1:6379> ttl s3
(integer) 594
127.0.0.1:6379> ttl s3
(integer) 592
127.0.0.1:6379> pttl s3
(integer) 588470
127.0.0.1:6379> pttl s3
(integer) 587497
127.0.0.1:6379> persist s3
(integer) 1
127.0.0.1:6379> ttl s3
(integer) -1
127.0.0.1:6379>
```

### KEYS

```
KEYS pattern
不要在生产环境中使用次命令，考虑使用SCAN
```

Supported glob-style patterns:

- `h?llo` matches `hello`, `hallo` and `hxllo`
- `h*llo` matches `hllo` and `heeeello`
- `h[ae]llo` matches `hello` and `hallo,` but not `hillo`
- `h[^e]llo` matches `hallo`, `hbllo`, ... but not `hello`
- `h[a-b]llo` matches `hallo` and `hbllo`

### MOVE

```
MOVE key db
将一个key移动到另一个db

```

### RANDOMKEY

随机获取一个key

### RENAME

```
RENAME key newkey
RENAMENX key newkey Rename a key, only if the new key does not exist

```

### SORT

```
TODO: sort指令的使用方式
```

### TYPE

获取key的类型

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

由于每个元素都是唯一的，所以同一元素不能在排序集中重复，但可以添加多个得分相同的不同元素。

当多个元素具有相同的分数时，它们将按字典顺序排序(它们仍然按照分数作为第一个键进行排序，但是，在局部，具有相同分数的所有元素将相对地按字典顺序排序)。

### ZADD

```
ZADD key [NX | XX] [GT | LT] [CH] [INCR] score member [score member...]
将具有指定分数的所有指定成员添加到存储在key处的排序集。可以指定多个分数/成员对。
如果指定的成员已经是排序集的成员，则更新分数，并将元素重新插入到正确的位置，以确保正确的排序。
score应该是双精度浮点数的字符串表示形式。+inf和-inf值也是有效值。
XX: 只更新已经存在的元素。不要添加新元素。
NX: 只添加新元素。不要更新已经存在的元素。
CH: 修改返回值的表示方式，将返回值从添加的新元素数量修改为更改的元素总数。更改的元素是新添加的元素和已经存在的元素并且元素的分数已经更新。


```

### ZCARD

```
返回有序集中元素的个数。
当key不存在时返回0
当key的类型不满足要求是报错

```

### ZCOUNT

```
ZCOUNT key min max
返回排序集中得分在min和max之间的元素个数。

127.0.0.1:6379> zcount s1 -inf +inf
(integer) 4
```

### ZLEXCOUNT

当一个已排序集中的所有元素都以相同的分数插入时，为了强制按字典顺序排序，该命令返回已排序集中在key处的元素数量，其值介于min和max之间。

元素被认为是按字节顺序从低到高的字符串排列的，如果公共部分相同，则长字符串被认为大于短字符串。

如果排序集中的元素具有不同的分数，则返回的元素未指定。

```
ZLEXCOUNT key min max
返回排序集中字母在min和max之间的元素个数。
min max 必须以( [ 开头，以确定是否是包含关系。min和max的特殊值+或-具有特殊含义或正无穷和负无穷字符串.

127.0.0.1:6379> zlexcount s1 - +
(integer) 4
127.0.0.1:6379> zlexcount s1 [a [b
(integer) 2
127.0.0.1:6379> zlexcount s1 [a (b
(integer) 1
```

### ZSCORE

```
ZSCORE key member

Returns the score of member in the sorted set at key.
If member does not exist in the sorted set, or key does not exist, nil is returned.
```

### ZRANK / ZREVRANK

```
zrank key member
zrevrank key member

返回存储在key的已排序集合中成员的秩，分数从低到高排序。
排名(或索引)以0为基础，这意味着得分最低的成员的排名为0。
```

### ZSCAN

See [`SCAN`](https://redis.io/commands/scan) for `ZSCAN` documentation.

### ZRANGE related

```
ZRANGE key start stop [WITHSCORES]
ZRANGEBYLEX key min max [LIMIT offset count]
ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]
ZREVRANGE key start stop [WITHSCORES]
ZREVRANGEBYLEX key max min [LIMIT offset count]
ZREVRANGEBYSCORE key max min [WITHSCORES] [LIMIT offset count]

以上命令都是获取有序集的成员。

ZRANGEBYLEX key min max [LIMIT offset count]
limit: 类似msyql中的 offset count

127.0.0.1:6379> zrangebylex s1 - + limit 1 2
1) "b"
2) "c"

------------------------------------------------------
ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]
min max 可以是 -inf +inf, 还有可选的前缀 ( 用来表示开区间

```

### ZPOP related

```
BZPOPMAX key [key ...] timeout
BZPOPMIN key [key ...] timeout
ZPOPMAX key [count]
ZPOPMIN key [count]

--------------------------------------------
BZPOP是阻塞模式，可以选择多个key，类似于BLPOP

127.0.0.1:6379> zpopmin s5 4
(empty list or set)
127.0.0.1:6379> zpopmin s1 2
1) "a"
2) "0"
3) "b"
4) "0"
```

### ZREM related

```
ZREM key member [member ...]
ZREMRANGEBYLEX key min max
ZREMRANGEBYRANK key start stop
ZREMRANGEBYSCORE key min max

移除元素，按照不同的方式
```

### ZINCRBY

```
ZINCRBY key increment member

Increments the score of member in the sorted set stored at key by increment. 
return: return new score

```

### ZUNIONSTORE / ZINTERSTORE

```
ZINTERSTORE destination numkeys key [key ...] [WEIGHTS weight] [AGGREGATE SUM|MIN|MAX]
ZUNIONSTORE destination numkeys key [key ...] [WEIGHTS weight] [AGGREGATE SUM|MIN|MAX]

在6.2.0 版本新增了如下commands:
ZDIFF numkeys key [key ...] [WITHSCORES]
ZDIFFSTORE destination numkeys key [key ...]
ZINTER numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE <SUM | MIN | MAX>] [WITHSCORES]
ZUNION numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE <SUM | MIN | MAX>] [WITHSCORES]

127.0.0.1:6379> zadd s2 5 d 6 d 7 f 8 g 9 h
(integer) 0
127.0.0.1:6379> zrange s2 0 -1 withscores
1) "d"
2) "6"
3) "f"
4) "7"
5) "g"
6) "8"
7) "h"
8) "9"
127.0.0.1:6379> zrange s1 0 -1 withscores
1) "a"
2) "11"
3) "b"
4) "12"
5) "c"
6) "13"
7) "d"
8) "14"
127.0.0.1:6379> ZUNIONSTORE s3 2 s1 s2 weights 1 2 aggregate sum
(integer) 7
127.0.0.1:6379> zrange s3 0 -1 withscores
 1) "a"
 2) "11"
 3) "b"
 4) "12"
 5) "c"
 6) "13"
 7) "f"
 8) "14"
 9) "g"
10) "16"
11) "h"
12) "18"
13) "d"
14) "26"
```

## Transactions

```
DISCARD -
summary: Discard all commands issued after MULTI

EXEC -
summary: Execute all commands issued after MULTI

MULTI -
summary: Mark the start of a transaction block

UNWATCH -
summary: Forget about all watched keys

WATCH key [key ...]
summary: Watch the given keys to determine execution of the MULTI/EXEC block
```

## Connection

```
AUTH password
summary: Authenticate to the server

ECHO message
summary: Echo the given string

PING [message]
summary: Ping the server

QUIT -
summary: Close the connection

SELECT index
summary: Change the selected database for the current connection

SWAPDB index index
summary: Swaps two Redis databases
```

## Server

```
client getname 
client setname conn-name
client id
client list
CLIENT KILL [ip:port] [ID client-id] [TYPE normal|master|slave|pubsub] [ADDR ip:port] [SKIPME yes/no]

client pause timeout
client reply on|off|skip

command 获取Redis命令详细信息数组
command count
command info command-name

debug object key
Value at:00007FCDBB028620 refcount:1 encoding:ziplist serializedlength:34 lru:797372 lru_seconds_idle:2440

info: server clients memory persistence stats replication cpu cluster keyspace

time: 返回server 时间
```

## Scripting

```
EVAL script numkeys key [key ...] arg [arg ...]
summary: Execute a Lua script server side

EVALSHA sha1 numkeys key [key ...] arg [arg ...]
summary: Execute a Lua script server side

SCRIPT DEBUG YES|SYNC|NO
summary: Set the debug mode for executed scripts.

SCRIPT EXISTS sha1 [sha1 ...]
summary: Check existence of scripts in the script cache.

SCRIPT FLUSH -
summary: Remove all the scripts from the script cache.

SCRIPT KILL -
summary: Kill the script currently in execution.

SCRIPT LOAD script
summary: Load the specified Lua script into the script cache.
```

