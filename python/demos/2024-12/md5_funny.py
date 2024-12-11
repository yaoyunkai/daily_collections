"""

计算 md5(x) = x

# 16 * 8
md5('a') = '0cc175b9c0f1b6a831c399e269772661'

select substr(md5_x, 1, 2) as prefix, count(*) as cnt
from md5_result
group by prefix;

created at 2024/12/3
"""

import hashlib
import sqlite3

ddl_sql = """
create table if not exists md5_result
(
    x     char(32) not null,
    md5_x char(32) not null
)
"""


def init_db(conn=None):
    if not conn:
        conn = sqlite3.connect('data.db')

    cursor = conn.cursor()
    try:
        cursor.execute(ddl_sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

    return conn


def close_conn(conn):
    if conn:
        try:
            conn.close()
        except:
            pass


def get_last_one_from_db(conn):
    cursor = conn.cursor()
    cursor.execute('select max(x) from md5_result')
    result = cursor.fetchone()
    result = result[0]

    print(f'get last one from db: {result}')
    return result


def insert_results_to_db(conn, results):
    """
    [
        [x, md5_x], [x1, md5_x1],
    ]

    """

    cursor = conn.cursor()
    try:
        cursor.executemany('insert into md5_result (x, md5_x) values (?, ?)', results)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()


def md5_demo(last_one: str, conn):
    if last_one is None:
        int_last_one = 0
    else:
        int_last_one = int.from_bytes(bytes.fromhex(last_one))
        int_last_one += 1

    start = '{:032x}'.format(int_last_one)
    print(f'start compute md5 with {start}')

    result_list = []
    max_cnt = 10000

    count = 10000 * 100
    # count = 58
    while count > 0:
        bytes_a = bytes.fromhex(start)

        md5_a = hashlib.md5(bytes_a).hexdigest()

        # print(f'{start} --> {md5_a}')
        if start == md5_a:
            print(f'found result {start} = {md5_a}')

        result_list.append((start, md5_a))

        int_a = int.from_bytes(bytes_a)
        int_a += 1
        start = '{:032x}'.format(int_a)
        count -= 1

        if len(result_list) == max_cnt:
            print(f'save md5 data to db')
            insert_results_to_db(conn, result_list)
            result_list.clear()

    if len(result_list) > 0:
        insert_results_to_db(conn, result_list)
        result_list.clear()

    close_conn(conn)


if __name__ == '__main__':
    # md5_demo('0000000000000000000000000000000f')
    # conn1 = init_db()
    # get_last_one_from_db(conn1)

    conn1 = init_db()
    md5_demo(get_last_one_from_db(conn1), conn1)
