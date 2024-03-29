"""
python的类型注解系统

TypeAlias

NewType: 创建新的类型

TypeVar: 泛型

Any: 类型与所有类型兼容

Self: current enclosed class

Union: 联合类型

Optional: 可选的

T = TypeVar('T')  # Can be anything
S = TypeVar('S', bound=str)  # Can be any subtype of str
A = TypeVar('A', str, bytes)  # Must be exactly str or bytes


def validate(cls, value: Any, field: 'ModelField', config: 'BaseConfig') -> 'AnyUrl':


================================================
Sequence Iterable

Optional

Union

Union[int, None]  -> Optional[int]

Callable[[int, int], int]


Literal['A', 'B']



Created at 2023/7/7
"""

from logging import Logger
from typing import Any, Generic, Type
from typing import List
from typing import TypeVar

T = TypeVar('T')  # Declare type variable "T"


def first(arr: List[T]) -> T:  # Function is generic over the TypeVar "T"
    return arr[0]


class LoggedVar(Generic[T]):
    def __init__(self, value: T, name: str, logger: Logger) -> None:
        self.name = name
        self.logger = logger
        self.value = value

    def set(self, new: T) -> None:
        self.log('Set ' + repr(self.value))
        self.value = new

    def get(self) -> T:
        self.log('Get ' + repr(self.value))
        return self.value

    def log(self, message: str) -> None:
        self.logger.info('%s: %s', self.name, message)


class A:
    name = 'A'

    def compare_other(self, other: 'A') -> bool:
        return id(self) == id(other)


def get_name(o: 'A') -> Any:
    return o.name


def get_name2(t: Type['A']) -> Any:
    return t.name


get_name(A())

get_name2(A)
