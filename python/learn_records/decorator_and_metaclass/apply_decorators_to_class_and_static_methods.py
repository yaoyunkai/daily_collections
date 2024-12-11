"""
给类或静态方法提供装饰器是很简单的，不过要确保装饰器在 @classmethod 或 @staticmethod 之前。

Create at 2023/3/27 21:31
"""
import time
from functools import wraps


# A simple decorator
def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("arg[0] is {}".format(args[0]))
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        print(end - start)
        return r

    return wrapper


# Class illustrating application of the decorator to different kinds of methods
class Spam:
    @timethis
    def instance_method(self, n):
        print(self, n)
        while n > 0:
            n -= 1

    @classmethod
    @timethis
    def class_method(cls, n):
        print(cls, n)
        while n > 0:
            n -= 1

    @staticmethod
    @timethis
    def static_method(n):
        print(n)
        while n > 0:
            n -= 1


if __name__ == '__main__':
    Spam().instance_method(5)
