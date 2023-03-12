# redis 持久化

redis支持两种不同的持久化方法：

- 快照 snapshotting：将存在于某一时刻的所有数据都写入磁盘。
- 只追加文件 append-only file：在执行写命令时，将被执行的写命令复制到磁盘。

## 相关的config

```
save 60 1000                        #A
stop-writes-on-bgsave-error no      #A
rdbcompression yes                  #A
dbfilename dump.rdb                 #A

appendonly no                       #B
appendfsync everysec                #B
no-appendfsync-on-rewrite no        #B
auto-aof-rewrite-percentage 100     #B
auto-aof-rewrite-min-size 64mb      #B

dir ./                              #C

A: SNAP
B: AOF
C: 两种持久化方式文件的保存位置
```

## SNAP

snap副本可以copy到其他服务器创建相同数据。

快照将被写入dbfilename选项指定的文件里面，并存储在dir指定的路径。

创建快照的方法：

- BGSAVE: 调用fork来创建一个子进程，子进程负责将快照写入磁盘，而父进程则继续处理命令。
- SAVE: 停止响应直到服务器完成快照创建。
- config的save选项：save 60 10000 从最近一次创建快照开始算起，当 60s之内有10000次写入，这个条件满足时，redis自动触发BGSAVE
- SHUTDOWN时，会执行SAVE
- 还有复制相关。

在只使用snap时，系统发生crash，用户将丢失最近一次生成快照后的更改的所有数据。

### 使用场景：