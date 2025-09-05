"""
协程预激

"""


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        # cr.next()
        next(cr)
        return cr

    return start
