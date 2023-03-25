# Redis事务

## 官方解释

事务中的所有命令都被序列化并按顺序执行。由另一个客户端发送的请求永远不会在Redis事务的执行过程中被服务。这保证了命令作为单独的隔离操作执行。

EXEC命令触发事务中所有命令的执行，因此，如果客户端在调用EXEC命令之前在事务上下文中失去与服务器的连接，则不会执行任何操作，相反，如果调用EXEC命令，则执行所有操作。

### Usage

使用MULTI命令输入Redis事务。该命令总是返回OK。此时，用户可以发出多个命令。Redis不会执行这些命令，而是将它们排队。所有命令都在调用EXEC时执行。

而调用DISCARD将刷新事务队列并退出事务。

```
> MULTI
OK
> INCR foo
QUEUED
> INCR bar
QUEUED
> EXEC
1) (integer) 1
2) (integer) 1
```

### Errors inside a transaction

- 命令可能无法排队，因此在调用EXEC之前可能会出现错误。例如，命令可能在语法上是错误的(错误的参数数量，错误的命令名，…)，或者可能存在一些临界条件
- 在调用EXEC之后，命令可能会失败，例如，因为我们对一个键执行了错误的操作(就像对一个字符串值调用了一个列表操作)。

在EXEC之后发生的错误不会以特殊的方式处理:即使某些命令在事务期间失败，所有其他命令也将执行。

需要注意的是，即使一个命令失败，队列中的所有其他命令也会被处理——Redis不会停止对命令的处理。

### Optimistic locking using check-and-set

WATCH用于为Redis事务提供检查和设置(**CAS**)行为。

监视键是为了检测它们的变化。如果在执行EXEC命令之前至少修改了一个被监视的键，则整个事务将中止，EXEC将返回Null应答，通知事务失败。

```
WATCH mykey
val = GET mykey
val = val + 1
MULTI
SET mykey $val
EXEC
```

那么WATCH到底是关于什么的呢?这是一个使EXEC有条件的命令:我们要求Redis只在所有被监视的键都没有被修改的情况下才执行事务。这包括客户端所做的修改，比如写命令，以及Redis本身所做的修改，比如过期或删除(不同的redis版本会有不同的体现)。如果在监视密钥和接收EXEC之间修改了密钥，则整个事务将被中止。

## 基本的redis事务

在redis中，被 `MULTI` 和 `EXEC` 命令所包围的所有命令会一个接一个执行，直到所有命令都执行完毕为止。

当redis从一个客户端那里接收到MULTI命令时，redis会将这个客户端之后发送的所有命令都放入到一个队列里面，直到这个客户端发送EXEC命令为止，然后Redis就会在不被打断的情况下，一个一个执行存储在队列里面的命令。

python客户端使用 `pipeline`来实现事务。

[code demo](../redis_in_action/chapter3_code.py)

## redis事务

https://redis.io/docs/manual/transactions/

由于简单的事务在MULTI命令被调用之前不会执行任何实际操作，所以用户将没办法根据读取到的数据来做决定。

无法以一致的形式读取数据将导致某一类型的问题变得难以解决。

在多个事务同时处理同一个对象时通常需要用到二阶提交(two-phase commit)。

在用户使用 `WATCH` 命令对键进行监视之后，直到用户执行 `EXEC` 命令的这段时间里面，如果有其他client对任何被监视的键进行的更新操作，那么当用户尝试执行exec命令的时候，事务将失败。

`UNWATCH`命令可以在watch命令执行之后，multi命令执行之前对连接进行重置。

`DISCARD`命令也可以在 multi命令执行之后，EXEC命令执行之前对连接进行重置。

用户在使用watch监视一个或多个键，接着使用multi开始一个新的事务，并将多个命令入队到事务队列后，仍可以通过discard来取消watch命令并清空所有已入队命令。

redis只会在数据已经被其他客户端抢先修改了的情况下，通知执行了WATCH命令的客户端，这种做法被称为乐观锁 optimistic locking

事务相关的命令：

```
WATCH
UNWATCH
MULTI
EXEC
DISCARD

```

## 非事务型流水线

在需要执行大量命令的情况下，即使命令实际上并不需要放在事务里面执行，但是为了通过一次发送所有命令，用户也可以将命令包裹在 MULTI和EXEC里面执行。但是 MULTI和EXEC也会消耗资源，并且可能会导致其他重要的命令被延迟执行。

可以使用 pipe = conn.pipeline(False) 来使用非事务流水线。这时就不会使用 MULTI和EXEC包裹命令了。

## benchmark

```
C:\Users\10524>redis-benchmark -c 1 -q
PING_INLINE: 13239.77 requests per second
PING_BULK: 13515.34 requests per second
SET: 13229.26 requests per second
GET: 13455.33 requests per second
INCR: 13399.44 requests per second
LPUSH: 12619.89 requests per second
RPUSH: 13020.83 requests per second
LPOP: 13003.90 requests per second
RPOP: 13090.72 requests per second
SADD: 13466.20 requests per second
HSET: 14649.87 requests per second
SPOP: 24582.11 requests per second
```

