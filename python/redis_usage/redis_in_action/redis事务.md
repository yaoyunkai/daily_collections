# Redis事务

## 基本的redis事务

在redis中，被 `MULTI` 和 `EXEC` 命令所包围的所有命令会一个接一个执行，直到所有命令都执行完毕为止。

当redis从一个客户端那里接收到MULTI命令时，redis会将这个客户端之后发送的所有命令都放入到一个队列里面，直到这个客户端发送EXEC命令为止，然后Redis就会在不被打断的情况下，一个一个执行存储在队列里面的命令。

python客户端使用 `pipeline`来实现事务。

[code demo](./chapter3_code.py)

