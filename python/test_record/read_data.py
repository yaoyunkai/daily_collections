"""
read test data

1. create model

----------------------------------------------------
table fields:

tst_id
bf_status

rec_time
sernum                  40 upper
uuttype                 40 upper
test_area               20 upper
test_result             pass_fail  SPF
run_time
test_failure
test_server
test_mode               PROD DEBUG
container

username
deviation

testr1name
testr1
testr2name
testr2
testr3name
testr3

tan
part_num
part_num2

hw_rev
hw_rev2
hw_rev3

product_id
vid

2. unique:
sernum tst_id test_result


"""

import json
from collections import OrderedDict

import MySQLdb

INSERT_SQL = """
insert into test_record (tst_id, bf_status, record_time, sernum, uuttype,
                         area, test_result, run_time, test_failure, test_server,
                         test_container, test_mode, username, deviation, testr1name,
                         testr1, testr2name, testr2)
values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""


def get_mysql_conn(db_name='demo3'):
    return MySQLdb.connect(host='localhost', port=3306, user='root', password='password', database=db_name)


def insert_test_records(test_records):
    mysql_conn = get_mysql_conn()
    cursor = mysql_conn.cursor()
    try:
        _n = cursor.executemany(INSERT_SQL, test_records)
        print('N is: {}'.format(_n))
        mysql_conn.commit()
    except MySQLdb.MySQLError:
        mysql_conn.rollback()
    mysql_conn.close()


def read_json_data(file_path, _petra=True):
    fp = open(file_path, mode='r')
    data = json.load(fp)

    json_result_list = []

    for idx, item in enumerate(data):
        _dict = OrderedDict()
        _dict['tst_id'] = item['tst_id']
        _dict['bf_status'] = 1 if item['bfstatus'] == 'YES' else 0
        _dict['record_time'] = item['rectime']
        _dict['sernum'] = item['sernum']
        _dict['uuttype'] = item['uuttype']
        _dict['area'] = item['area']
        _dict['test_result'] = item['passfail']
        _dict['run_time'] = item['attributes'].get('RUNTIME', 0)
        _dict['test_failure'] = item['attributes'].get('TEST', '')
        _dict['test_server'] = item['machine']
        _dict['test_container'] = item['attributes'].get('CONTAINER', 'NULL')
        _dict['test_mode'] = item['mode']
        _dict['username'] = item['attributes'].get('USERNAME', 'NULL')
        _dict['deviation'] = item['attributes'].get('DEVIATION', 'D000000')
        _dict['testr1name'] = item['attributes'].get('TESTR1NAME', '')
        _dict['testr1'] = item['attributes'].get('TESTR1', '')
        _dict['testr2name'] = item['attributes'].get('TESTR2NAME', '')
        _dict['testr2'] = item['attributes'].get('TESTR2', '')

        if _petra:
            _dict['testr2name'] = item['attributes'].get('TESTR3NAME', '')
            _dict['testr2'] = item['attributes'].get('TESTR3', '')

        json_result_list.append(_dict)

    return json_result_list


if __name__ == '__main__':
    pass
