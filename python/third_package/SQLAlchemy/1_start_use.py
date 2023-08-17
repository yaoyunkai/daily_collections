"""
建立连接

Connection
Result

Session


text() for Write SQL

-------------------------------------------------------
Session & Engine

engine.connect
engine.begin

result.mappings


class Base(DeclarativeBase)

Base.metadata

从数据库中获取Table的结构
some_table = Table("some_table", metadata_obj, autoload_with=engine)


"""

import sqlalchemy
from sqlalchemy.orm import Session

# print(sqlalchemy.__version__)

"""
sqlite: 哪种数据库 dialect
pysqlite: DBAPI

lazy connection

"""
engine = sqlalchemy.create_engine("sqlite+pysqlite:///:memory:", echo=True)

with engine.connect() as conn:
    """
    not committed automatically
    Connection.commit()
    
    """
    result = conn.execute(sqlalchemy.text("select 'hello world'"))
    print(result.all())

with engine.connect() as conn:
    """
    commit as you go
    
    executemany
    
    """
    conn.execute(sqlalchemy.text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        sqlalchemy.text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()

with engine.begin() as conn:
    conn.execute(
        sqlalchemy.text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
    )

with engine.connect() as conn:
    """
    sqlalchemy.engine.cursor.CursorResult
    sqlalchemy.engine.row.Row
    
    result = conn.execute(text("select x, y from some_table"))
    
    for x, y in result:
    
    for row in result:
    x = row[0]
    
    for row in result:
    y = row.y
    
    for dict_row in result.mappings():
    x = dict_row["x"]
    y = dict_row["y"]
    
    
    """
    result = conn.execute(sqlalchemy.text("SELECT x, y FROM some_table"))
    print(result)
    for row in result:
        print(type(row))
        print(f"x: {row.x}  y: {row.y}")

with engine.connect() as conn:
    result = conn.execute(sqlalchemy.text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

stmt = sqlalchemy.text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")

with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
