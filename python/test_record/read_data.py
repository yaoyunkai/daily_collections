"""
read test data

1. create model

----------------------------------------------------
table fields

rec_time
tst_id
bf_status

sernum     40 upper
uuttype    40 upper
test_area  20 upper
test_result  pass_fail  SPF
run_time
test_failure
test_server

test_mode PROD DEBUG
container
username
deviation

tan
hw_rev
part_num

testr1
testr1_name

pid
vid


"""

import json
from pprint import pprint

demo_data = 'Petra_sys_bst.json'


def read_json_data():
    fp = open(demo_data, mode='r')
    data = json.load(fp)
    for idx, item in enumerate(data):
        if idx == 4:
            pprint(item)


if __name__ == '__main__':
    read_json_data()
