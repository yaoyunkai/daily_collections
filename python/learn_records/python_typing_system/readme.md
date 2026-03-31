# python的类型系统

> links: https://typing.readthedocs.io/en/latest/index.html

当你使用一个泛型（Generic type）但没有提供具体的类型参数时，类型检查器（如 mypy）会默认将其参数视为 Any。

**函数的返回值问题**: 

当函数无返回值时: None  
当函数无法返回时: NoReturn

## 类型约束

- Optional 
- Union 
- Literal
- Annotated
- NewType
- TypeAlias
- Final
- TypedDict
- TypeVar
- Generic
- Any

一个使用 Literal 的例子

```python
ALLOW_TYPES = Literal["xml", "json", "protobuf", "html", 0]


# @validate_call
def get_results(result_type: ALLOW_TYPES):
    pass

# 1. pydantic validate_call
# 2. typing.get_args
# 3. match case



```

### Annotated 最常见的三大使用场景:

- 数据校验与约束`(Pydantic)` `Age = Annotated[int, Field(ge=18, le=100)]`
- Web 框架的参数解析与路由
- 数据库 ORM 映射

### NewType 的使用场景

在静态类型检查时，将它们视为完全不同的类型以防止混用；但在程序实际运行时，它们依然是原生类型，没有任何性能损耗。

为基础数据类型赋予强烈的业务语义，防止具有相同底层类型但业务含义不同的变量被意外混用。

### Generic 对类本身的影响

当你让类继承了 `Generic[T]` 后，typing 模块会在底层为你的类自动实现一个特殊魔术方法 `__class_getitem__`。

继承 Generic 会对类本身注入几个特殊的双下划线（dunder）属性。
- `__parameters__`: 记录该泛型类使用了哪些类型变量（例如它会记录这里用到了类型变量 T）
- `__orig_bases__`: 记录类定义时的原始基类信息（保留了泛型参数的痕迹）。

