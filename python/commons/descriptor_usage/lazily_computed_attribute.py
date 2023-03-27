"""
定义一个延迟属性的一种高效方法是通过使用一个描述器类

如果一个描述器仅仅只定义了一个 __get__() 方法的话，它比通常的具有更弱的绑定。
特别地，只有当被访问属性不在实例底层的字典中时 __get__() 方法才会被触发。


Created at 2023/3/27
"""
import math


class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


class Circle:
    def __init__(self, radius):
        # 半径
        self.radius = radius

    @lazyproperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2

    @lazyproperty
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius


if __name__ == '__main__':
    c = Circle(4)
    print(c.radius)
    print(c.area)

    print(c.area)
