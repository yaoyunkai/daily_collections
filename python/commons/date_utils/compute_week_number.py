"""
https://webspace.science.uu.nl/~gent0113/calendar/isocalendar.htm

Created at 2023/2/18
"""

import datetime

BASE_2023 = 27


def test_func():
    d = datetime.datetime(2023, 1, 2)
    print(d)
    print(d.isocalendar())


def get_year_week_number(date_obj=None):
    if date_obj:
        assert isinstance(date_obj, (datetime.date, datetime.datetime))
    else:
        date_obj = datetime.datetime.now()
    year, weeknum, _ = date_obj.isocalendar()

    return '{0:0>2}{1:0>2}'.format(
        year - 2023 + BASE_2023, weeknum
    )


if __name__ == '__main__':
    _ret = get_year_week_number()
    print(_ret)
