"""

metaclass

在创建类的时候会调用：
    __prepare__: ???
    __new__ : name, bases, attrs, **kwargs
    __init__: name, bases, attrs, **kwargs

在类实例化时会调用:
    __call__:


__init_subclass__:
    当所在类派生子类时此方法就会被调用。cls 将指向新的子类。


Create at 2023/3/27 21:52
"""


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
        cls.__str__ = print_object

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
        return super().__call__()


class Bar(object, metaclass=Foo, demo=1234):
    name = 12345


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

    d2 = AustralianPhilosopher()
