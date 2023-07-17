"""


Created at 2023/7/14
"""
import datetime
import re
from typing import Optional

_PT_DATE = re.compile(r'(\d{4})-(\d{1,2})(?:-(\d{1,2}))?')
_PT_DATETIME = re.compile(r'(\d{4})-(\d{1,2})-(\d{1,2})T(\d{1,2}):(\d{1,2}):(\d{1,2})')
_T = 'T'

_MONTH_DAY_DICT = {
    1: 31,
    2: [28, 29],
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}


def is_valid_staff_id(staff_id: str) -> bool:
    return re.match(r'[FXG]\d{7}', staff_id) is not None


def is_valid_english_name(person_name: str) -> bool:
    return re.match(r"^[A-Za-z\s'-]+$", person_name) is not None


def is_valid_chinese_name(person_name: str) -> bool:
    return re.match(r"^[\u4e00-\u9fa5]{2,4}$", person_name) is not None


def is_leap_year(year: int) -> bool:
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return True
    else:
        return False


class DateTime:
    """
    don't directly initial the class

    use classmethod:
        from_date_string

    一种数据结构:
        可以表示时间的范围，
        也可以表示时间节点

    如果是范围, 那么久不需要两个点了
    如果是时间点，那么久需要两个点来表示

    """

    year: int
    month: int
    day: Optional[int]
    hour: Optional[int]
    minute: Optional[int]
    second: Optional[int]

    @classmethod
    def _init(cls, year, month, day=None, hour=None, minute=None, second=None):
        obj = cls()
        obj.year = year
        obj.month = month
        obj.day = day
        obj.hour = hour
        obj.minute = minute
        obj.second = second
        return obj

    def __str__(self):
        if self.hour is None and self.minute is None and self.second is None:
            if self.day is not None:
                return '{}-{}-{}'.format(self.year, self.month, self.day)
            else:
                return '{}-{}'.format(self.year, self.month)
        return '{}-{}-{}T{}:{}:{}'.format(
            self.year, self.month, self.day,
            self.hour, self.minute, self.second
        )

    # def __eq__(self, other: 'DateTime'):
    #     if self.year != other.year:
    #         return False
    #     if self.month != other.month:
    #         return False

    @classmethod
    def _valid_time(cls, hour: int, minute: int, second: int) -> bool:
        if not 0 <= hour < 24:
            return False
        if not 0 <= minute < 60:
            return False
        if not 0 <= second < 60:
            return False
        return True

    @classmethod
    def _valid_year_month(cls, year: int, month: int) -> bool:
        if not 0 < year <= 9999:
            return False
        if not 1 <= month <= 12:
            return False
        return True

    @classmethod
    def _valid_date(cls, year: int, month: int, day: int) -> bool:
        if not 0 < year <= 9999:
            return False
        if not 1 <= month <= 12:
            return False
        if not 1 <= day <= 31:
            return False

        if month == 2:
            if is_leap_year(year):
                day_range = 29
            else:
                day_range = 28
        else:
            day_range = _MONTH_DAY_DICT[month]

        if day > day_range:
            return False

        return True

    @classmethod
    def from_date_string(cls, date_string: str) -> Optional['DateTime']:
        """
        date string format:

        year-month
        year-month-day
        year-month-dayTh:m:s

        """
        date_string = date_string.strip()
        if not date_string:
            return None

        if 'T' in date_string:
            pattern = _PT_DATETIME
        else:
            pattern = _PT_DATE

        match_result = pattern.match(date_string)
        if not match_result:
            return None

        date_list = match_result.groups()
        if date_list[2] is None:
            date_list = [int(ch) for ch in date_list[:2]]
            if not cls._valid_year_month(*date_list):
                return None
            return cls._init(*date_list)

        date_list = [int(ch) for ch in date_list]
        if len(date_list) > 3:
            if not cls._valid_time(*date_list[-3:]):
                return None

        if not cls._valid_date(*date_list[:3]):
            return None

        return cls._init(*date_list)

    @classmethod
    def from_datetime_now(cls):
        # 时区问题: 应该和数据库的时区一致
        _now = datetime.datetime.now()
        return cls._init(
            _now.year,
            _now.month,
            _now.day,
            _now.hour,
            _now.minute,
            _now.second
        )


if __name__ == '__main__':
    print(DateTime.from_date_string('2023-02-3'))
    print(DateTime.from_date_string('2023-02'))
    print(DateTime.from_date_string('2023-22'))
    print(DateTime.from_date_string('2023-12-33'))

    print(DateTime.from_date_string('2023-12-12T12:44:23'))
    print(DateTime.from_date_string('2023-12-12T24:00:00'))
    print(DateTime.from_date_string('2023-2-29'))
    print(DateTime.from_date_string('2024-2-29'))
    print(DateTime.from_date_string('2023-04-31'))
    print(DateTime.from_date_string('2024-2-29T23:59:60'))
    print(DateTime.from_date_string('2024-2-29T23:59:59'))
    print(DateTime.from_date_string('2023-7-17T14:38:23'))
    print(DateTime.from_datetime_now())
