# PostgreSQL 修炼之道

## chp4. psql tool

psql 相关的参数：

```
 -d, --dbname=DBNAME      指定要连接的数据库
 -h, --host=主机名         数据库服务器主机或socket目录(默认："本地接口")
 -p, --port=端口           数据库服务器的端口(默认："5432")
 -U, --username=用户名     指定数据库用户名
 -w, --no-password        永远不提示输入口令
 -W, --password           强制口令提示 (自动)

psql -h localhost -p 5432 -U test1 -d demo1
```

查看数据库：

```
demo1=# \l
                                                      数据库列表
   名称    |  拥有者  | 字元编码 | Locale Provider | 校对规则 | Ctype | ICU Locale | ICU Rules |       存取权限
-----------+----------+----------+-----------------+----------+-------+------------+-----------+-----------------------
 demo1     | test1    | UTF8     | libc            | en-US    | en-US |            |           |
 postgres  | postgres | UTF8     | libc            | en-US    | en-US |            |           |
 template0 | postgres | UTF8     | libc            | en-US    | en-US |            |           | =c/postgres          +
           |          |          |                 |          |       |            |           | postgres=CTc/postgres
 template1 | postgres | UTF8     | libc            | en-US    | en-US |            |           | =c/postgres          +
           |          |          |                 |          |       |            |           | postgres=CTc/postgres
(4 行记录)
```

查看表：

```
demo1=# \d
                      关联列表
 架构模式 |          名称          |  类型  | 拥有者
----------+------------------------+--------+--------
 public   | demo_order             | 数据表 | test1
 public   | demo_order_id_seq      | 序列数 | test1
 public   | demo_pay_record        | 数据表 | test1
 public   | demo_pay_record_id_seq | 序列数 | test1
 public   | serial_sequence        | 数据表 | test1
 public   | test_record            | 数据表 | test1
 public   | test_record_id_seq     | 序列数 | test1
(7 行记录)
```

### chp4.3 psql常见命令

`\h` 该命令用于查询SQL语句的语法

```
demo1=# \h create user
命令：       CREATE USER
描述：       定义一个新数据库角色
语法：
CREATE USER 名称 [ [ WITH ] 选项 [ ... ] ]

选项可以是

      SUPERUSER | NOSUPERUSER
    | CREATEDB | NOCREATEDB
    | CREATEROLE | NOCREATEROLE
    | INHERIT | NOINHERIT
    | LOGIN | NOLOGIN
    | REPLICATION | NOREPLICATION
    | BYPASSRLS | NOBYPASSRLS
    | CONNECTION LIMIT 连接限制
    | [ ENCRYPTED ] PASSWORD '口令' | PASSWORD NULL
    | VALID UNTIL '时间戳'
    | IN ROLE 角色名称 [, ...]
    | IN GROUP 角色名称 [, ...]
    | ROLE 角色名称 [, ...]
    | ADMIN 角色名称 [, ...]
    | USER 角色名称 [, ...]
    | SYSID uid

URL: https://www.postgresql.org/docs/16/sql-createuser.html
```

`\d` 命令将显示每个匹配“pattern”（表、视图、索引、序列）的信息，包括对象中所有的列、各列的数据类型、表空间（如果不是默认的）和所有特殊属性（诸如“NOT NULL”或默认值等）等。

```
demo1=# \d
                      关联列表
 架构模式 |          名称          |  类型  | 拥有者
----------+------------------------+--------+--------
 public   | demo_order             | 数据表 | test1
 public   | demo_order_id_seq      | 序列数 | test1
 public   | demo_pay_record        | 数据表 | test1
 public   | demo_pay_record_id_seq | 序列数 | test1
 public   | serial_sequence        | 数据表 | test1
 public   | test_record            | 数据表 | test1
 public   | test_record_id_seq     | 序列数 | test1
(7 行记录)


demo1=# \d demo_order_id_seq
              序列数 "public.demo_order_id_seq"
  类型   | 起始值 | 最小值 |   最大值   | 增量 | 循环? | 缓存
---------+--------+--------+------------+------+-------+------
 integer |      1 |      1 | 2147483647 |    1 | no    |    1
属于: public.demo_order.id


demo1=# \d demo_order
                                         数据表 "public.demo_order"
       栏位       |           类型           | 校对规则 |  可空的  |                  预设
------------------+--------------------------+----------+----------+----------------------------------------
 id               | integer                  |          | not null | nextval('demo_order_id_seq'::regclass)
 order_no         | character varying(32)    |          | not null |
 order_created_at | timestamp with time zone |          | not null | now()
 order_status     | character varying(32)    |          | not null | 'pending'::character varying
索引：
    "demo_order_pkey" PRIMARY KEY, btree (id)
    "demo_order_order_no_key" UNIQUE CONSTRAINT, btree (order_no)


demo1=# \d+ demo_order
                                                           数据表 "public.demo_order"
       栏位       |           类型           | 校对规则 |  可空的  |                  预设                  |   存储   | 压缩 | 统计目标 | 描述
------------------+--------------------------+----------+----------+----------------------------------------+----------+------+----------+------
 id               | integer                  |          | not null | nextval('demo_order_id_seq'::regclass) | plain    |      |          |
 order_no         | character varying(32)    |          | not null |                                        | extended |      |          |
 order_created_at | timestamp with time zone |          | not null | now()                                  | plain    |      |          |
 order_status     | character varying(32)    |          | not null | 'pending'::character varying           | extended |      |          |
索引：
    "demo_order_pkey" PRIMARY KEY, btree (id)
    "demo_order_order_no_key" UNIQUE CONSTRAINT, btree (order_no)
访问方法 heap
```

指定客户端的编码：

```
demo1=# \encoding utf8
demo1=# \encoding gbk
```

使用`\x`命令可以把按行展示的数据变成按列展示：

```
demo1=# \x
扩展显示已打开.
demo1=# \x
扩展显示已关闭.
```

## chp5. 数据类型

