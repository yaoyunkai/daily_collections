"""

metaclass

在创建类的时候会调用：
    __prepare__: ???
    __new__ : name, bases, attrs, **kwargs
    __init__: name, bases, attrs, **kwargs

在类实例化时会调用:
    __call__: cls: 基类对象, 和 __init__ 中的参数


__init_subclass__:
    当所在类派生子类时此方法就会被调用。cls 将指向新的子类。


Create at 2023/3/27 21:52
"""
import threading


def print_object(self, ):
    return 'Object'


class Foo(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        """
        cls: is subclass object

        :param name: subclass name
        :param bases: subclass' super class
        :param attrs:
        :param kwargs:
        """
        # super().__init__()
        print('call __init__')
        # print(cls, name, bases, attrs, kwargs)
        # cls.__str__ = print_object

        super().__init__(name, bases, attrs)

    def __new__(mcs, name, bases, attrs, **kwargs):
        """
        mcs: Foo self object

        :param name: 子类的名字
        :param bases: 子类继承的类
        :param attrs:
        :param kwargs:
        """
        print('call __new__ ')
        print('attrs: {}'.format(attrs))
        ret = super().__new__(mcs, name, bases, attrs)
        return ret

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        print('call __prepare__')
        return super().__prepare__(name, bases)

    def __call__(cls, *args, **kwargs):
        print('call __call__')
        print(cls, args, kwargs)
        return super().__call__(*args, **kwargs)


class Bar(object, metaclass=Foo, demo=1234):
    name = 12345

    def __init__(self, name, age, **kwargs):
        pass


class SingletonMeta(type):
    _instances = None
    _lock = threading.RLock()

    def __call__(cls, *args, **kwargs):
        with SingletonMeta._lock:
            if SingletonMeta._instances is None:
                SingletonMeta._instances = {}

            if cls not in SingletonMeta._instances:
                instance = super().__call__(*args, **kwargs)
                SingletonMeta._instances[cls] = instance
        return SingletonMeta._instances[cls]


class Parent:
    _lock = None
    pass


class Singleton(Parent, metaclass=SingletonMeta):
    pass


class Philosopher:
    def __init_subclass__(cls, **kwargs):
        print('call __init_subclass__')
        cls.default_name = kwargs.pop('default_name', None)
        super().__init_subclass__(**kwargs)


class AustralianPhilosopher(Philosopher, default_name="Bruce"):
    pass


if __name__ == '__main__':
    # bar = Bar()
    # bar = Bar()
    # print(bar)
    # print(vars(Bar))

    bar = Bar(123, 213, ab=12344, ac=123444)

    s1 = Singleton()
    s2 = Singleton()
    s3 = Singleton()
    s4 = Singleton()

    print(s1 == s3)
