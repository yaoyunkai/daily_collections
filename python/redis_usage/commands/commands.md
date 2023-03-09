# Redis comands

## Strings

### append

```
APPEND key value

return: 追加操作后的字符串长度。

key不存在的话会创建一个新的key
```

### bitcount

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

### bitop

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

### bitpos

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

### getbit

```
GETBIT key offset

返回存储在key的字符串值中偏移处的位值。

offset: 0表示第一位 不支持负一，使用-1时会报错，那么取最后一位可以使用 strlen * 8 - 1

```

### getrange

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

### getset(已弃用)

设置键的字符串值并返回其旧值

return: the old value stored at `key`, or `nil` when `key` did not exist.

### get&set related

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

### setbit

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

### setrange

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

### strlen

获取存储在键中的值的长度,不存在的key返回0

