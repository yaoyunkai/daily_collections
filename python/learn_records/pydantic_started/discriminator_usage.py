"""

允许你根据某个字段的值来确定应该使用联合中的哪个具体模型。
这对于解析和验证具有多态性质的数据结构非常有用，


created at 2024/12/19
"""

from typing import Literal

from pydantic import BaseModel, Field


class Cat(BaseModel):
    pet_type: Literal['cat']
    age: int


class Dog(BaseModel):
    pet_type: Literal['dog']
    age: int


class Model(BaseModel):
    pet: Cat | Dog = Field(discriminator='pet_type')


print(Model.model_validate({'pet': {'pet_type': 'cat', 'age': 12}}))
