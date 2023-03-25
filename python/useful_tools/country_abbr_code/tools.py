"""


Create at 2023/2/19 18:20
"""

import MySQLdb

from data import DATA  # NOQA


def get_mysql_conn(db_name='demo3'):
    return MySQLdb.connect(host='localhost', port=3306, user='root', password='password', database=db_name)


def check_code_exists(code2_str):
    _sql = """select code2 from country_abbr_code where code2 = %s limit 1"""

    if len(code2_str) != 2:
        return False

    conn = get_mysql_conn()
    cursor = conn.cursor()
    cursor.execute(_sql, (code2_str,))
    rows = cursor.fetchone()
    conn.close()

    return rows is not None


if __name__ == '__main__':
    print(check_code_exists('CN'))
