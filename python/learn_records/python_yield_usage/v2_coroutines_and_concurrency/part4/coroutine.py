"""
协程预激

"""
import functools


def coroutine(func):
    @functools.wraps(func)
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr

    return start
