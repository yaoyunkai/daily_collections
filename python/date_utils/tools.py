"""
日期相关

"""
import datetime


def get_datetime_now():
    return datetime.datetime.now()


def human_datetime_delta(datetime_obj, mode='ZH'):
    """


    :param datetime_obj:
    :param mode: ZH or CN
    :return:
    """

    now = get_datetime_now()

    if datetime_obj > now:
        raise ValueError('given datetime rather than current datetime')
