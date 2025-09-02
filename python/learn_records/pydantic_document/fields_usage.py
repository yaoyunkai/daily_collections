"""
字段的使用

Filed.default_factory 可调用对象。

validate_default=True

=============================================

字段别名

Field(alias='foo')
Field(validation_alias='foo')
Field(serialization_alias='foo')


Field(repr=False) 在 __str__ __repr__ 是否出现。


Strict Mode 严格模式


frozen  是否可以更改



created at 2024/12/19
"""
import random
from pprint import pprint  # NOQA
from typing import List, Annotated

from pydantic import BaseModel
from pydantic import Field
from pydantic import ValidationError
from pydantic import WithJsonSchema


def get_demo_value():
    return random.randint(1, 100)


def receive_data(val: dict) -> str:
    """
    已验证的数据
    已验证的数据将作为字典传递

    """

    print(f'get value is {val}')

    return 'HH'


class MyModel(BaseModel):
    name: str = Field(frozen=True)
    str1: Annotated[str, Field(strict=True), WithJsonSchema({'extra': 'data'})]
    field2: List[Annotated[int, Field(gt=0)]]
    name2: str = Field(default="Peter")

    value3: int = Field(default_factory=get_demo_value)
    value4: str = Field(default_factory=receive_data)


class Foo(BaseModel):
    name: str = Field(alias='username')


if __name__ == '__main__':
    pprint(MyModel.model_json_schema())

    d1 = dict(
        name='Tom',
        str1='Peter',
        field2=[1, 2, ],
        # value3=44,
    )

    try:
        obj = MyModel.model_validate(d1)
    except ValidationError as e:
        pprint(e.json())
        raise

    print(obj.value3)

    obj2 = Foo(username='Peter')
    # obj3 = Foo(name='Peter')
    pprint(obj2.model_dump())
    pprint(obj2.model_dump(by_alias=True))
