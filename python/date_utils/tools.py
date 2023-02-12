"""
日期相关


"""
import datetime

STR_HUMAN_READABLE = (
    ['{} year ago', '{} years ago', '{}年前'],
    ['{} month ago', '{} months ago', '{}个月前'],
    ['{} day ago', '{} days ago', '{}天前'],
    ['{} hour ago', '{} hours ago', '{}小时前'],
    ['{} minute ago', '{} minutes ago', '{}分钟前'],
    ['just now', 'just now', '刚刚'],
)


def get_current_datetime():
    return datetime.datetime.now()


def is_singular(num):
    """
    是否为单数

    :param num:
    :return:
    """
    return num == 1


def human_datetime_delta(datetime_obj: datetime.datetime, mode='ZH'):
    """


    :param datetime_obj:
    :param mode: ZH or EN
    :return:
    """

    def _get_print(f_index, _number):
        s_index = 1
        if is_singular(_number):
            s_index = 0
        if mode == 'ZH':
            s_index = 2

        if f_index == -1 or f_index == (len(STR_HUMAN_READABLE) - 1):
            return STR_HUMAN_READABLE[f_index][s_index]

        return STR_HUMAN_READABLE[f_index][s_index].format(_number)

    if mode not in ['ZH', 'EN']:
        raise ValueError('language mode must be "ZH" "EN"')

    now = get_current_datetime()
    if datetime_obj > now:
        raise ValueError('given datetime rather than current datetime')

    if datetime_obj.year != now.year:
        return _get_print(0, now.year - datetime_obj.year)
    if datetime_obj.month != now.month:
        return _get_print(1, now.month - datetime_obj.month)
    if datetime_obj.day != now.day:
        return _get_print(2, now.day - datetime_obj.day)
    if datetime_obj.hour != now.hour:
        return _get_print(3, now.hour - datetime_obj.hour)
    if datetime_obj.minute != now.minute:
        return _get_print(4, now.minute - datetime_obj.minute)
    return _get_print(5, -1)


if __name__ == '__main__':
    demo1 = get_current_datetime() - datetime.timedelta(days=5)
    demo3 = get_current_datetime() - datetime.timedelta(seconds=5)
    demo2 = get_current_datetime() - datetime.timedelta(days=11 * 30)
    print(human_datetime_delta(demo1, mode='EN'))
    print(human_datetime_delta(demo2, mode='EN'))
    print(human_datetime_delta(demo3))
