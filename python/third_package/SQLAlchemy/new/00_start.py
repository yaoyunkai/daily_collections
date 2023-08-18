"""
Created at 2023/8/17

psycopg2

TODO diff from connection between session

结束事务后，会话实际上并不保留连接对象。下次需要对数据库执行 SQL 时，它会从引擎获取一个新的 Connection。

"""

from sqlalchemy import create_engine, text

engine = create_engine(
    url="postgresql+psycopg2://user1:password@localhost/simple_230808", echo=True
)


def test_get_connection():
    with engine.connect() as conn:
        result = conn.execute(text("select 'hello world'"))
        print(result.scalar())


def test_commit():
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        conn.commit()


def test_begin():
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
        )


def test_fetch_rows():
    conn = engine.connect()

    result = conn.execute(text("select x, y from some_table"))
    for dict_row in result.mappings():
        # x = dict_row["x"]
        # y = dict_row["y"]
        print(dict_row)


def test_sql_params():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
        for row in result:
            print(f"x: {row.x}  y: {row.y}")


def test_sql_multi_params():
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
        )
        conn.commit()


def test_session():
    from sqlalchemy.orm import Session

    stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
    with Session(engine) as session:
        result = session.execute(stmt, {"y": 6})
        for row in result:
            print(f"x: {row.x}  y: {row.y}")


if __name__ == "__main__":
    # test_get_connection()
    # test_begin()
    # test_fetch_rows()
    # test_sql_params()
    # test_sql_multi_params()
    test_session()
