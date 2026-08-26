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

### chp5.1 数据类型介绍

#### 数据类型的输入与转换

对于一些简单的数据类型，如数字或字符串，使用一般的方法输入就可以,

对于复杂的数据类型，可以按照“类型名”加上单引号括起来的类型值格式来输入:

```sql
select 1, 3.1415, 'hello world';
select bit '11101001111';
select integer '1' + integer '2';

select cast('5' as int), cast('2025-01-03' as date);
select '5'::int, '2025-01-03'::date;
```

### chp5.2 boolean

SQL使用三值的布尔逻辑：TRUE、FALSE和NULL，其中NULL代表“未知”。

```sql
expression is true;
expr is not true;
expr is false;
expr is not false;
expr is unknown;
expr is not unknown;
```

### chp5.3 数值类型

数值类型是最常用的几种数据类型之一，分为整型、浮点型、精确小数等类型

| 类型名称          | 存储空间 | 描述             |
| ----------------- | -------- | ---------------- |
| smallint          | 2byte    | 小范围的整数     |
| int / intgeter    | 4byte    |                  |
| bigint            | 8byte    |                  |
| numeric / decimal | 变长     | 用户声明的精度。 |
| real              | 4byte    |                  |
| double precision  | 8byte    |                  |
| serial            | 4byte    |                  |
| bigserial         | 8byte    |                  |

整数类型有3种：smallint、int、bigint.

精确的小数类型可用numeric、numeric(m,n)、numeric(m)表示：`select '455.56'::numeric(10, 4);`

- **Precision（精度 - m）**：整个数值中所有有效数字的总位数（小数点左边和右边的数字总和）。
- **Scale（标度 - n）**：小数点右边的数字位数。

推荐使用 `numeric` 的场景

- **金融和货币计算**：如商品价格、账户余额、税率、利息等。在这些场景中，浮点数（如 `real` 或 `double precision`）的四舍五入误差是不可接受的。
- **需要绝对精确的科学计算**：对计算精度有极高要求的特定领域。

避免使用 `numeric(m)` 存储纯整数。

数据类型real和double precision是不精确的、变精度的数字类型。

#### 货币类型

货币类型可以存储固定小数的货币数目，与浮点数不同，它是完全保证精度的。其输出格式与参数lc_monetary的设置有关，不同的国家其货币输出格式也不相同。

```sql
select '12.34'::money;
show lc_monetary;
set lc_monetary  = 'en_US.UTF-8';

```

### chp5.4 字符串类型

| 类型                              | 描述               |
| --------------------------------- | ------------------ |
| character varying(n) / varchar(n) | 变长               |
| character(n) / char(n)            | 定长               |
| text                              | 变长，无长度限制。 |

在PostgreSQL中，定长的character(n)与varchar(n)没有差别。故在大多数情况下，建议使用text或varchar。

在 PostgreSQL 中，`varchar(n)` 中的 `n` 限制的是**字符数（Characters）**

我们可以通过 PostgreSQL 的内置函数来直观地看到这种区别：

- **获取字符长度**：使用 `length('你好')` 或 `char_length('你好')`，返回的结果是 **2**。
- **获取字节长度**：使用 `octet_length('你好')`，在 UTF-8 字符集下返回的结果是 **6**。

### chp5.7 日期类型

| Name                                        | Storage Size | Description                           | Low Value        | High Value      | Resolution    |
| ------------------------------------------- | ------------ | ------------------------------------- | ---------------- | --------------- | ------------- |
| `timestamp [ (p) ] [ without time zone ]` | 8 bytes      | both date and time (no time zone)     | 4713 BC          | 294276 AD       | 1 microsecond |
| `timestamp [ (p) ] with time zone`      | 8 bytes      | both date and time, with time zone    | 4713 BC          | 294276 AD       | 1 microsecond |
| `date`                                      | 4 bytes      | date (no time of day)                 | 4713 BC          | 5874897 AD      | 1 day         |
| `time [ (p) ] [ without time zone ]`    | 8 bytes      | time of day (no date)                 | 00:00:00         | 24:00:00        | 1 microsecond |
| `time [ (p) ] with time zone`           | 12 bytes     | time of day (no date), with time zone | 00:00:00+1559    | 24:00:00-1559   | 1 microsecond |
| `interval [ fields ] [ (p) ]`       | 16 bytes     | time interval                         | -178000000 years | 178000000 years | 1 microsecond |

PostgreSQL中的时间类型可以精确到秒以下, `time`、`timestamp`、`interval`接受一个可选的精度值p以指明秒域中小数部分的位数。如果没有明确的默认精度，对于timestamp和interval类型，p的取值范围是0～6。

在SQL中，任何日期或者时间的文本输入都需要由“日期/时间”类型加单引号括起来的字符串组成:

```sql
type [ (p) ] 'value';

select date '2022-12-21' as my_date;

# 显示日期格式
show datestyle;
```

CST在PostgreSQL中代表Central Standard Time (USA) UT-6:00，缩写可以查询视图“pg_timezone_abbrevs”：

```sql
select * from pg_timezone_abbrevs where abbrev = 'CST';
```

### chp5.8 枚举类型

创建一个枚举类型：

```sql
CREATE TYPE week AS ENUM ('Sun','Mon','Tues','Wed','Thur','Fri', 'Sat');
CREATE TABLE duty(person text, weekday week);
INSERT INTO duty values（'张三', 'Sun'）;
INSERT INTO duty values（'李四', 'Mon'）;
INSERT INTO duty values（'王二', 'Tues'）;
INSERT INTO duty values（'赵五', 'Wed'）;
```

使用如下命令查询所有的枚举类型：

```sql
select * from pg_enum;

17240,17238,1,Sun
17242,17238,2,Mon
17244,17238,3,Tues
17246,17238,4,Wed
17248,17238,5,Thus
17250,17238,6,Fri
17252,17238,7,Sat

```

