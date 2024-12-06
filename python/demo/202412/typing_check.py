"""

Optional Union

Optional[str]   Union[str, None]

abc.Mapping




created at 2024/12/6
"""
from typing import Any, TypeAlias


def double(x: Any) -> Any:
    return x * 2


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


FromTo: TypeAlias = tuple[str, str]

if __name__ == '__main__':
    o2 = T2()
    f1(o2)

    o1 = T1()
    f2(o1)

    o0 = object()
    f3(o0)
    f3(o1)
    f3(o2)
