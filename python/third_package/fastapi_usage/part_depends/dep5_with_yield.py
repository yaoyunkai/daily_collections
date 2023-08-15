"""

do some extra steps after finishing.

和 with 一起使用

@contextmanager
def managed_resource(*args, **kwds):
    # Code to acquire resource, e.g.:
    resource = acquire_resource(*args, **kwds)
    try:
        yield resource
    finally:
        # Code to release resource, e.g.:
        release_resource(resource)

发送响应前，只执行 yield之前的代码，
发送响应后，执行 finally的代码


Created at 2023/8/15
"""
