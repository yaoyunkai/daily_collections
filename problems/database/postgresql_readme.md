# PostgreSQL

## table inspection

```sql
\d+ your_table_name

# 或者查询info schema
SELECT 
    column_name, 
    data_type, 
    character_maximum_length, 
    column_default, 
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_name = 'your_table_name';
```

使用 sqlalchemy的inspector 方法。

```python
from sqlalchemy import create_engine, inspect

# 1. 创建数据库引擎
engine = create_engine("postgresql+psycopg://user:password@localhost/dbname")

# 2. 创建检查器 (Inspector)
inspector = inspect(engine)

# 3. 获取指定表的所有列信息
columns = inspector.get_columns("orders")

# 4. 打印列信息
for col in columns:
    print(f"列名: {col['name']}")
    print(f"类型: {col['type']}")
    print(f"允许为空: {col['nullable']}")
    print(f"默认值: {col['default']}")
    print("-" * 20)

# 还可以获取索引、主键等其他信息：
# pk = inspector.get_pk_constraint("orders")
# indexes = inspector.get_indexes("orders")
```

### python client

Psycopg 3 和 Psycopg 2.

## datetime 字段

在数据库层面设置了 `timestamp with time zone` 后，**在 Python 代码中插入或更新数据时，需要传入“带时区信息”（Timezone-aware）的 `datetime` 对象**。

```python
import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # 对应 PostgreSQL 的 timestamp with time zone
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True)
    )
```

数据库的连接URL:

```python
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg://xxxxx:xxx@localhost:5432/demo1"

engine = create_engine(
    DATABASE_URL,
    # 通过 connect_args 传递底层 psycopg 驱动的参数
    connect_args={
        "options": "-c timezone=UTC"
    },
    echo=True  # 开启 SQL 日志输出，方便调试
)
```

### python层的默认值和数据库层的默认值写法

- default 
- server_default

```python
# 1. 静态标量默认值
status: Mapped[str] = mapped_column(default="active")

# 2. 动态可调用对象 (Callable)
# 注意：这里传的是函数本身 (uuid.uuid4)，而不是函数调用 (uuid.uuid4())
# 每次插入新记录时，SQLAlchemy 都会调用这个函数
api_key: Mapped[str] = mapped_column(default=uuid.uuid4)

# 3. 动态时间
created_at: Mapped[datetime] = mapped_column(default=get_utc_now)

created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
```

## 字符类型

以下是具体的写法和区别：

1. `text` 类型 (无长度限制的字符串)

**概念**：对应 PostgreSQL 中的 `TEXT`。它用于存储任意长度的字符串，没有最大长度限制。 **SQLAlchemy 类型**：`sqlalchemy.Text`

```python
content: Mapped[str] = mapped_column(Text)
```

2. 定长 `char` 类型 (固定长度字符串)

**概念**：对应 PostgreSQL 中的 `CHAR(n)` 或 `CHARACTER(n)`。它用于存储固定长度的字符串。如果插入的字符串长度小于 `n`，PostgreSQL 会在末尾**自动填充空格**以达到长度 `n`。 **SQLAlchemy 类型**：`sqlalchemy.CHAR`

```python
country_code: Mapped[str] = mapped_column(CHAR(2))
```

**推荐使用 `TEXT` 或 `VARCHAR(n)`**

```python
username: Mapped[str] = mapped_column(String(50))
```

### 固定长度+校验

最佳实践：`String(18)` + `CheckConstraint`

```python
id_card: Mapped[str] = mapped_column(
    String(18), 
    # 1. 数据库层面的长度严格校验：必须正好是 18 位
    CheckConstraint("char_length(id_card) = 18", name="ck_user_id_card_len"),
    # 2. 身份证号通常是唯一的，建议加上唯一索引
    unique=True,
    # 3. 如果经常通过身份证号查询用户，建议加上普通索引（unique=True 默认会建索引，这里仅为说明）
    index=True,
    # 4. 身份证号通常不允许为空
    nullable=False
)
```

### 编码和排序的相关问题

PostgreSQL 提供了三种主要的字符类型：`CHAR(n)`、`VARCHAR(n)` 和 `TEXT`。

在 PostgreSQL 的底层 C 语言源码中，这三种类型实际上使用的是**完全相同的数据结构**（叫做 `varlena`，即可变长度数组）。

**字符 (Character) vs 字节 (Byte)**

在 PostgreSQL 中，`VARCHAR(10)` 限制的是 **10 个字符（Characters）**，而不是 10 个字节。 这意味着，无论您存入的是 10 个英文字母、10 个汉字，还是 10 个 Emoji 表情，它们都能完美存入 `VARCHAR(10)` 中。PG 会自动处理底层的字节长度。

**编码 encoding**

PostgreSQL 的 `UTF8` 编码就是标准的、原生的、支持 1~4 字节的完整 UTF-8。

PostgreSQL 采用了 **服务器编码 (Server Encoding)** 和 **客户端编码 (Client Encoding)**。

**排序规则 (Collation)**

- 默认的本地化排序 (Linguistic Collation)
- `C` Collation (Byte-wise Collation)

```python
order_no: Mapped[str] = mapped_column(String(32, collation='C'), index=True)
```

## python not null & database not null

SQLAlchemy 2.0 引入了基于类型提示（Type Hints）的全新声明方式.

在 2.0 版本中，数据库的 `NOT NULL` 约束**默认由 Python 的类型提示（Type Hint）决定**。

## 状态类型的字段

**在 Python 层使用枚举（Enum），并在数据库层映射为字符串（VARCHAR/CHAR）**。

```python
import enum

class OrderStatus(str, enum.Enum):
    DRAFT = "S"      # 草稿 (Start / Save)
    RUNNING = "R"    # 正在执行 (Running)
    DONE = "D"       # 已完成 (Done)

status: Mapped[OrderStatus] = mapped_column(
    # 1. 限制数据库中该列的长度为 1 (因为 S, R, D 都是单字符)
    String(1), 

    # 2. Python 层的默认值：创建订单时如果不传状态，默认是草稿
    default=OrderStatus.DRAFT,

    # 3. 数据库层的默认值：防止其他系统直接写库时漏传字段
    server_default=OrderStatus.DRAFT.value,

    # 4. 状态不能为空
    nullable=False,

    # 5. 状态字段经常用于过滤查询 (如查询所有正在执行的订单)，建议加索引
    index=True 
)
```

## python table 增量更新的问题

`Base.metadata.create_all(engine)` **绝对不支持**增量更新

在 SQLAlchemy 生态中，处理数据库结构增量更新：**Alembic**。

## 数据库优先的模式(从db生成sqlalchemy表结构)

**推荐工具：`sqlacodegen`** 这是一个非常强大的开源工具。

```
# 将数据库中的所有表生成为 SQLAlchemy 2.0 风格的模型，并保存到 models.py 中
sqlacodegen postgresql+psycopg://user:password@localhost:5432/demo1 --generator declarative --outfile models.py
```

## Tags 类型字段

tags这种类型的字段使用 m2m 还是 arrays ?
为了在 Python 中完美支持列表的修改（如 `append` 或 `remove`），我们必须引入 SQLAlchemy 的 `MutableList`。

```python
tags: Mapped[list[str]] = mapped_column(
    # 用 MutableList 包装 ARRAY，内部元素类型为 String(50)
    MutableList.as_mutable(ARRAY(String(50))),

    # 数据库层默认值：PostgreSQL 的空数组语法是 '{}'
    server_default="{}",

    # 建议不允许为 NULL，空状态用空列表 [] 表示，这样在代码里处理更方便，不用写 if tags is None
    nullable=False 
)
```

sqlalchemy对array相关的操作：

```python
from sqlalchemy import select

# 场景 1：查询 tags 中包含 "python" 的所有记录 (最常用)
# 对应 SQL: WHERE tags @> ARRAY['python']
stmt1 = select(Simple1).where(
    Simple1.tags.contains(["python"])
)

# 场景 2：查询 tags 包含 "python" 且包含 "fastapi" 的记录 (包含多个)
stmt2 = select(Simple1).where(
    Simple1.tags.contains(["python", "fastapi"])
)

# 场景 3：查询 tags 和 ["java", "go"] 有任何交集 (Overlap) 的记录
# 对应 SQL: WHERE tags && ARRAY['java', 'go']
stmt3 = select(Simple1).where(
    Simple1.tags.overlap(["java", "go"])
)

# 场景 4：查询 tags 数组长度大于 3 的记录
# 对应 SQL: WHERE array_length(tags, 1) > 3
stmt4 = select(Simple1).where(
    func.array_length(Simple1.tags, 1) > 3
)
```

## 创建database的参数

### Template (模板数据库)

- **原理解释**：在 PostgreSQL 中，创建新数据库的底层逻辑是**“克隆”**。它并不是凭空生成的，而是完整复制一个现有的数据库。
- **作用**：默认情况下，它会复制名为 `template1` 的系统自带数据库。如果您在 `template1` 中安装了某些扩展（比如地理空间插件 PostGIS），那么以后基于它创建的所有新数据库都会自动带上 PostGIS。
- **最佳实践**：保持默认（通常为空或 `template1`），除非您有自定义的模板库。

### Tablespace (表空间)

- **原理解释**：表空间定义了数据库文件在**服务器磁盘上的实际物理路径**。
- **作用**：默认是 `pg_default`（通常位于 PG 安装目录下的 `data` 文件夹）。在企业级架构中，DBA 可能会创建多个表空间，例如把频繁读写的热点数据库放在 SSD 表空间，把历史归档数据库放在机械硬盘 (HDD) 表空间。
- **最佳实践**：如果您只有一块硬盘或在本地开发，保持默认 `pg_default`。

### Strategy (创建策略) - *PG 15 引入的新特性*

- **原理解释**：既然建库是“克隆”模板，那么怎么克隆呢？
  - `WAL_LOG`（默认）：通过写入预写日志 (WAL) 的方式逐块复制。**优点**：非常安全，且允许在复制期间其他用户继续连接和操作模板数据库。
  - `FILE_COPY`：直接在操作系统层面复制底层文件。**优点**：速度极快。**缺点**：复制期间会锁定模板数据库，不允许其他操作。
- **最佳实践**：保持默认 `WAL_LOG`。

----

这四个参数 (`encoding`, `locale provider`, `collation`, `character type`) 是高度绑定的，它们共同决定了您的数据库如何认识和处理文字。

### Encoding (字符集编码)

- **原理解释**：决定了字符在底层磁盘上是如何转换为**二进制字节**的。
- **最佳实践**：**永远、绝对选择 `UTF8`**。它支持全球所有语言以及 Emoji 表情，是现代软件开发的唯一标准。

### Locale Provider (本地化提供程序) - *PG 15 引入的重要特性*

- **原理解释**：当数据库需要对字符串进行排序或大小写转换时，它需要一套“规则字典”。这个字典由谁提供？
  - `libc`（传统默认）：使用**操作系统**自带的 C 标准库提供规则。**致命隐患**：如果您的操作系统升级了（比如 Ubuntu 升级），操作系统的字典可能会变，这会导致数据库里原本建好的文本索引瞬间失效（数据损坏风险）。
  - `icu`（现代推荐）：使用独立于操作系统的 **ICU (International Components for Unicode)** 库。它的规则是跨平台且极其稳定的。
- **最佳实践**：强烈推荐选择 **`icu`**，以保证数据库在跨服务器迁移或系统升级时的绝对稳定。

### Collation (排序规则 / LC_COLLATE)

- **原理解释**：决定了字符串在执行 `ORDER BY`、`>`、`<` 时的**先后顺序**。比如，大写 `A` 和小写 `a` 谁在前面？中文是按拼音排还是按笔画排？
- **常见选项**：
  - `en_US.utf8` 或 `zh_CN.utf8`：按照人类语言习惯排序（中文按拼音）。**缺点**：极其消耗 CPU，且普通的 B-Tree 索引可能不支持 `LIKE 'abc%'` 查询。
  - `C` 或 `POSIX`：完全抛弃人类语言规则，直接按照底层字节的 ASCII/二进制值比大小。
- **最佳实践**：
  - 如果您**不需要**在数据库层面进行复杂的拼音或字母表排序（通常排序应该交给前端或后端代码做），**强烈建议填写 `C`**。这会带来巨大的性能提升。
  - 如果必须按人类语言排序，根据您的 Locale Provider，填写对应的标识（如 `zh-Hans-CN` (ICU) 或 `zh_CN.utf8` (libc)）。

### Character Type (字符分类 / LC_CTYPE)

- **原理解释**：决定了数据库如何**识别和分类字符**。比如，执行 `UPPER('a')` 时，数据库怎么知道 `'a'` 的大写是 `'A'`？在使用正则表达式时，什么算作“字母”，什么算作“数字”？
- **最佳实践**：这个参数**必须与 Collation 保持一致**。如果您在 Collation 填了 `C`，这里也必须填 `C`。如果填了 `en_US.utf8`，这里也一样。

----

在 PostgreSQL 中，创建数据库时 `collation` 和 `character type` 对应的实际参数是 **`LC_COLLATE`** 和 **`LC_CTYPE`**。

- collation:影响 `ORDER BY`、`WHERE col = 'xxx'`、`< > <= >=` 等文本比较操作。
- cahracter type: 影响大小写转换函数：`UPPER()`、`LOWER()`、`INITCAP()` , 影响字符判断函数：`ISALPHA()`、`ISDIGIT()`、`ISUPPER()` 等

```sql
SELECT datname, datcollate, datctype FROM pg_database WHERE datname = current_database();
```

### ** encoding, LC_CTYPE & LC_COLLATE

> **`ENCODING` 决定“字符怎么变成字节存进去”，`LC_CTYPE` 决定“这个字符属于什么类别（字母/数字/空格/标点），以及大小写怎么转换”。**

| 设置         | 底层作用                  | 依赖组件                             | 影响范围                                                     |
| ------------ | ------------------------- | ------------------------------------ | ------------------------------------------------------------ |
| `ENCODING`   | 字符 ↔ 字节序列的映射规则 | PG 内部编码转换器                    | 存储合法性、网络传输、客户端解码                             |
| `LC_CTYPE`   | 字符分类 & 大小写变形     | 操作系统 C 库（`glibc` 等）的 locale | `UPPER/LOWER`、正则分类 `\w`/`[:alpha:]`、单词边界、IS ALPHA 等 |
| `LC_COLLATE` | 字符串排序 & 比较规则     | 操作系统 C 库的 locale               | `ORDER BY`、`=`/`<`/`>`、索引扫描、`LIKE` 行为               |

**LC_CTYPE 影响了什么东西**

PostgreSQL 自身不实现字符分类逻辑，而是将字符串交给操作系统的 LC_CTYPE locale，调用 C 标准库函数（如 `iswalpha()`, `towlower()`, `iswdigit()` 等）。

## 如何查看某个database的相关属性

```sql
SELECT datname, 
       pg_encoding_to_char(encoding) AS encoding, 
       datcollate, 
       datctype 
FROM pg_database 
WHERE datname = 'template1';
```

如何查看数据库支持的collation：

```sql
SELECT * FROM pg_collation where collname like 'zh-%';
```

## SQL语言

### 数据定义

#### 默认值

在 PostgreSQL 数据库中，如果在创建表或添加字段时没有明确指定，字段的默认属性是 **NULL**（即允许为空）。

#### 标识列

要创建标识列，可在`CREATE TABLE`中使用`GENERATED ... AS IDENTITY`子句，例如：

```sql
CREATE TABLE people (
    id bigint GENERATED ALWAYS AS IDENTITY,
    ...,
);

CREATE TABLE people (
    id bigint GENERATED BY DEFAULT AS IDENTITY,
    ...,
);

-- 写入数据

INSERT INTO people (name, address) VALUES ('A', 'foo');
INSERT INTO people (name, address) VALUES ('B', 'bar');

INSERT INTO people (id, name, address) VALUES (DEFAULT, 'C', 'baz');
```

#### 生成列

生成列有两种：存储型和虚拟型。存储型生成列在写入时（插入或更新时）计算，并像普通列一样占用存储空间。虚拟生成列不占用存储空间，而是在读取时计算。

```sql
CREATE TABLE people (
    ...,
    height_cm numeric,
    height_in numeric GENERATED ALWAYS AS (height_cm / 2.54)
);
```

#### 约束

检查约束
非空约束
唯一约束
主键
外键
排他约束

#### 系统列

- `tableoid` 

  包含该行的表的 OID。`tableoid`可以与`pg_class`的`oid`列连接，以取得表名。

- `xmin` 

  插入该行版本的事务标识（事务 ID）。（行版本是某一行的一个具体状态；对同一逻辑行的每次更新都会创建一个新的行版本。）

- `cmin` 

  插入事务中的命令标识符（从0开始）。

- `xmax` 

  删除事务的标识（事务 ID）；对于未删除的行版本则为 0。对于一个可见的行版本，该列也可能是非零值。这通常表示删除事务尚未提交，或者一次删除尝试被回滚了。

- `cmax` 

  删除事务中的命令标识符，或者为0。

- `ctid` 

  行版本在其表中的物理位置。注意尽管`ctid`可以被用来非常快速地定位行版本，但是一个行的`ctid`会在被更新或者被`VACUUM FULL`移动时改变。因此，不应将`ctid`用作行标识符。应使用主键来标识逻辑行。

