"""
water
fire
wind
earth


"""
import sqlite3


def get_sql_connection():
    return sqlite3.connect('table.db')


init_data = [
    'Water',  # 💧
    'Fire',  # 🔥
    'Wind',  # 🌬️
    'Earth',  # 🌍
]


class Runner:
    def __init__(self):
        self.conn = get_sql_connection()


def check_things_exists(conn: 'sqlite3.Connection', name: str):
    stmt = "select 1 from things where name = :name limit 1"
    cur = conn.execute(stmt, {'name': name})
    result = cur.fetchone()
    return result is not None


def insert_one_thing(conn: 'sqlite3.Connection', name: str, emoji: str):
    stmt = "insert into things (name, emoji) values (:name, :emoji)"


def insert_things(conn: 'sqlite3.Connection', item_list: list):
    pass


if __name__ == '__main__':
    check_things_exists(get_sql_connection(), 'Water')
