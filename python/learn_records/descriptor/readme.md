# 属性描述符

某个类实现了 `__get__` `__set__` `__delete__` 的就叫做属性描述符类。

可选地，描述器可以具有 `__set_name__()` 方法。这仅在描述器需要知道创建它的类或分配给它的类变量名称时使用。（即使该类不是描述器，只要此方法存在就会调用。）

在属性查找期间，描述器由点运算符调用。如果使用 `vars(some_class)[descriptor_name]` 间接访问描述器，则返回描述器实例而不调用它。

描述器仅在用作类变量时起作用。放入实例时，它们将失效。

描述器的主要目的是提供一个挂钩，允许存储在类变量中的对象控制在属性查找期间发生的情况。

传统上，调用类控制查找过程中发生的事情。描述器反转了这种关系，并允许正在被查询的数据对此进行干涉。

## full demo

### 自定义验证器

验证器是一个用于托管属性访问的描述器。在存储任何数据之前，它会验证新值是否满足各种类型和范围限制。如果不满足这些限制，它将引发异常，从源头上防止数据损坏。

```python
from abc import ABC, abstractmethod

class Validator(ABC):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass
```

1. `OneOf` 验证值是一组受约束的选项之一。
1. `Number` 验证值是否为 [`int`](https://docs.python.org/zh-cn/3/library/functions.html#int) 或 [`float`](https://docs.python.org/zh-cn/3/library/functions.html#float)。根据可选参数，它还可以验证值在给定的最小值或最大值之间。
1. `String` 验证值是否为 [`str`](https://docs.python.org/zh-cn/3/library/stdtypes.html#str)。根据可选参数，它可以验证给定的最小或最大长度。它还可以验证用户定义的 [predicate](https://en.wikipedia.org/wiki/Predicate_(mathematical_logic))。

```python
class OneOf(Validator):

    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f'Expected {value!r} to be one of {self.options!r}')

class Number(Validator):

    def __init__(self, minvalue=None, maxvalue=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f'Expected {value!r} to be an int or float')
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(
                f'Expected {value!r} to be at least {self.minvalue!r}'
            )
        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(
                f'Expected {value!r} to be no more than {self.maxvalue!r}'
            )

class String(Validator):

    def __init__(self, minsize=None, maxsize=None, predicate=None):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Expected {value!r} to be an str')
        if self.minsize is not None and len(value) < self.minsize:
            raise ValueError(
                f'Expected {value!r} to be no smaller than {self.minsize!r}'
            )
        if self.maxsize is not None and len(value) > self.maxsize:
            raise ValueError(
                f'Expected {value!r} to be no bigger than {self.maxsize!r}'
            )
        if self.predicate is not None and not self.predicate(value):
            raise ValueError(
                f'Expected {self.predicate} to be true for {value!r}'
            )
```

## technical-tutorial

### 描述器协议

```
descr.__get__(self, obj, type=None) -> value

descr.__set__(self, obj, value) -> None

descr.__delete__(self, obj) -> None
```

非数据描述器：仅定义了 `__get__`

数据描述器：如果一个对象定义了 `__set__()` 或 `__delete__()`，则它会被视为数据描述器。

为了使数据描述器成为只读的，应该同时定义 `__get__()` 和 `__set__()` ，并在 `__set__()` 中引发 `AttributeError`。用引发异常的占位符定义 `__set__()` 方法使其成为数据描述器。

### 调用方式

描述器可以通过 `d.__get__(obj)` 或 `desc.__get__(None, cls)` 直接调用。

但更常见的是通过属性访问自动调用描述器。

表达式 `obj.x` 在命名空间的链中查找``obj`` 的属性 `x`。如果搜索在实例 `__dict__` 之外找到描述器，则根据下面列出的优先级规则调用其 `__get__()` 方法。

调用的细节取决于 `obj` 是对象、类还是超类的实例。

#### 在实例上调用

实例查找通过命名空间链进行扫描，数据描述器的优先级最高，其次是实例变量、非数据描述器、类变量，最后是 `__getattr__()` （如果存在的话）。

如果 `a.x` 找到了一个描述器，那么将通过 `desc.__get__(a, type(a))` 调用它。

```python
def find_name_in_mro(cls, name, default):
    "Emulate _PyType_Lookup() in Objects/typeobject.c"
    for base in cls.__mro__:
        if name in vars(base):
            return vars(base)[name]
    return default

def object_getattribute(obj, name):
    "Emulate PyObject_GenericGetAttr() in Objects/object.c"
    null = object()
    objtype = type(obj)
    cls_var = find_name_in_mro(objtype, name, null)
    descr_get = getattr(type(cls_var), '__get__', null)
    if descr_get is not null:
        if (hasattr(type(cls_var), '__set__')
            or hasattr(type(cls_var), '__delete__')):
            return descr_get(cls_var, obj, objtype)     # data descriptor
    if hasattr(obj, '__dict__') and name in vars(obj):
        return vars(obj)[name]                          # instance variable
    if descr_get is not null:
        return descr_get(cls_var, obj, objtype)         # non-data descriptor
    if cls_var is not null:
        return cls_var                                  # class variable
    raise AttributeError(name)
```

在 `__getattribute__()` 方法的代码中没有调用 `__getattr__()` 的钩子。

这就是直接调用 `__getattribute__()` 或调用 `super().__getattribute__` 会彻底绕过 `__getattr__()` 的原因。

当 `__getattribute__()` 引发 AttributeError 时，点运算符和 getattr() 函数负责调用 `__getattr__()`。它们的逻辑封装在一个辅助函数中：

```python
def getattr_hook(obj, name):
    "Emulate slot_tp_getattr_hook() in Objects/typeobject.c"
    try:
        return obj.__getattribute__(name)
    except AttributeError:
        if not hasattr(type(obj), '__getattr__'):
            raise
    return type(obj).__getattr__(obj, name)             # __getattr__
```

#### 在类对象上调用

像 `A.x` 这样的点操作符查找的逻辑在 `type.__getattribute__()` 中。步骤与 `object.__getattribute__()` 相似，但是实例字典查找改为搜索类的 [method resolution order](https://docs.python.org/zh-cn/3/glossary.html#term-method-resolution-order)。

如果找到了一个描述器，那么将通过 `desc.__get__(None, A)` 调用它。

#### 通过super调用

super 的点操作符查找的逻辑在 [`super()`](https://docs.python.org/zh-cn/3/library/functions.html#super) 返回的对象的 `__getattribute__()` 方法中。

类似 `super(A, obj).m` 形式的点分查找将在 `obj.__class__.__mro__` 中搜索紧接在 `A` 之后的基类 `B`，然后返回 `B.__dict__['m'].__get__(obj, A)`。如果 `m` 不是描述器，则直接返回其值。

#### 总结

描述器的机制嵌入在 object，type 和 super() 的 `__getattribute__()` 方法中。

- 描述器由 `__getattribute__()` 方法调用。
- 类从 `object`，`type` 或 `super()` 继承此机制。
- 由于描述器的逻辑在 `__getattribute__()` 中，因而重写该方法会阻止描述器的自动调用。
- `object.__getattribute__()` 和 `type.__getattribute__()` 会用不同的方式调用 `__get__()`。前一个会传入实例，也可以包括类。后一个传入的实例为 `None` ，并且总是包括类。
- 数据描述器始终会覆盖实例字典。
- 非数据描述器会被实例字典覆盖。

## 纯python等价实现

### property

```python
class Property:
    "Emulate PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc
        self._name = ''

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError(f"property '{self._name}' has no getter")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError(f"property '{self._name}' has no setter")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError(f"property '{self._name}' has no deleter")
        self.fdel(obj)

    def getter(self, fget):
        prop = type(self)(fget, self.fset, self.fdel, self.__doc__)
        prop._name = self._name
        return prop

    def setter(self, fset):
        prop = type(self)(self.fget, fset, self.fdel, self.__doc__)
        prop._name = self._name
        return prop

    def deleter(self, fdel):
        prop = type(self)(self.fget, self.fset, fdel, self.__doc__)
        prop._name = self._name
        return prop
```

### 函数和方法

Python 的面向对象功能是在基于函数的环境构建的。通过使用非数据描述器，这两方面完成了无缝融合。

在调用时，存储在类词典中的函数将被转换为方法。方法与常规函数的不同之处仅在于对象实例被置于其他参数之前。

- 函数 method：类里面的叫函数
- 方法 function：全局的叫方法

```python
class Function:
    ...

    def __get__(self, obj, objtype=None):
        "Simulate func_descr_get() in Objects/funcobject.c"
        if obj is None:
            return self
        return MethodType(self, obj)
```

