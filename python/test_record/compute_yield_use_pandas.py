"""


Created at 2023/2/27
"""
import pandas as pd

from insert_data import get_mysql_conn


def read_data():
    conn = get_mysql_conn()

    data = pd.read_sql('select record_time, sernum, uuttype, area, test_result '
                       'from test_record order by record_time', conn)

    data.set_index('record_time', inplace=True)

    first_data = data.drop_duplicates(subset=['sernum', 'area'], keep='first')

    conn.close()

    print(first_data)


if __name__ == '__main__':
    read_data()
