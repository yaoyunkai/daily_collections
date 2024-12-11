"""

属性访问

instance.X

__getattr__(instance, X)

__getattribute__(instance, X)

getattr(o, name)


Created at 2023/3/27
"""


class Wrap:
    def __init__(self, name):
        self._name = name

    def __get__(self, instance, owner):
        print('call descriptor __get__')

    # def __set__(self, instance, value):
    #     pass


class Demo:
    name = Wrap('name')

    def __init__(self, name):
        self.name = name

    def __getattribute__(self, item):
        print('call instance __getattribute__')
        # return object.__getattribute__(self, item)
        return 345

    def __getattr__(self, item):
        print('call instance __getattr__')
        return 123


if __name__ == '__main__':
    d = Demo('Tom')
    print(d.name1)
