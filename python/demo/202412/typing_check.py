"""

Optional Union

Optional[str]   Union[str, None]

abc.Mapping




created at 2024/12/6
"""
from random import shuffle
from typing import Any, TypeAlias, TypeVar, Sequence
from typing import TypedDict

T = TypeVar('T')
FromTo: TypeAlias = tuple[str, str]


def sample(population: Sequence[T], size: int) -> list[T]:
    if size < 1:
        raise ValueError('size must be >= 1')
    result = list(population)
    shuffle(result)
    return result[:size]


def double(x: Any) -> Any:
    return x * 2


#  typedict
class BookDict(TypedDict):
    isbn: str
    title: str
    authors: list[str]
    pagecount: int


class T1:
    pass


class T2(T1):
    pass


def f1(p: T1) -> None:
    pass


def f2(p: T2) -> None:
    pass


def f3(p: Any) -> None:
    pass


if __name__ == '__main__':
    o2 = T2()
    f1(o2)

    o1 = T1()
    f2(o1)

    o0 = object()
    f3(o0)
    f3(o1)
    f3(o2)
