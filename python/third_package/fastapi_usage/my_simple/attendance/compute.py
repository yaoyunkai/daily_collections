"""

上班时间:
午休时间:
午休结束时间:
下班时间:
加班开始时间:
加班结束时间:

午休扣除时间:
晚餐扣除时间:


1.  8:29 18:01
2. 8:29 12:01  12:31 18:01
3. 8:29 9:00   10:00      12:01  12:31 18:01
4. 8:29 9:00   10:00      12:01  12:31    3:00 5:00        18:01

one person record list


Created at 2023/7/19
"""
import datetime
import re
from collections import namedtuple
from typing import List
from typing import Optional

rule = {
    'start_time': '08:30',
    'mid_start': '12:00',
    'mid_end': '13:30',
    'end_time': '18:00',
}

HourMinute = namedtuple('HourMinute', 'hour minute')

PT_DATETIME = re.compile(r'(\d{4})-(\d{1,2})-(\d{1,2})[T ](\d{1,2}):(\d{1,2}):(\d{1,2})')


def get_hour_minutes(value: str) -> 'HourMinute':
    _tmp = value.split(':')
    return HourMinute(
        int(_tmp[0].strip()), int(_tmp[1].strip())
    )


def convert_to_datetime(value: str) -> Optional[datetime.datetime]:
    match_result = PT_DATETIME.match(value)
    if not match_result:
        return None

    return datetime.datetime(
        *[int(i) for i in match_result.groups()]
    )


demo1 = [
    {
        "staff_id": "F1336930",
        "staff_name": "Tim",
        "record_time": "2023-07-15T08:25:01",
        "record_machine": "A",
        "record_type": "in",
        "id": 1
    },
    {
        "staff_id": "F1336930",
        "staff_name": "Tim",
        "record_time": "2023-07-15T18:03:41",
        "record_machine": "B",
        "record_type": "out",
        "id": 2
    },
]


def compute(att_rule: dict, att_record_list: List[dict]):
    """
    前提条件是获取到了某一天的打卡记录，并且按时间升级排序

    """

    for record in att_record_list:
        record_time = record['record_time']
        record_type = record['record_type']
