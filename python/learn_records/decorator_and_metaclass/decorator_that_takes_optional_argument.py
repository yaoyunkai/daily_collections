"""


Created at 2023/3/27
"""

import logging
from functools import wraps, partial


def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    if func is None:
        return partial(logged, level=level, name=name, message=message)

    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.log(level, logmsg)
        return func(*args, **kwargs)

    return wrapper


# Example use
@logged
def add(x, y):
    return x + y


"""
add = logged(add)
这时候，被装饰函数会被当做第一个参数直接传递给 logged 装饰器。 
因此，logged() 中的第一个参数就是被包装函数本身。所有其他参数都必须有默认值。


"""


@logged(level=logging.CRITICAL, name='example')
def spam():
    print('Spam!')


"""
spam = logged(level=logging.CRITICAL, name='example')(spam)


"""