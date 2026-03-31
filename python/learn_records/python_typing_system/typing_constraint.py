"""
类型约束

"""

import typing
from typing import Literal, NewType, Optional, Union


def use_optional():
    maybe_a_string: str | None = "abcdef"
    maybe_a_string: Optional[str] = None


class Foo:
    pass


class Bar:
    pass


def return_bar_or_foo() -> Union[Foo, Bar]:
    a = 12
    if a > 15:
        return Foo()
    else:
        return Bar()


ALLOW_TYPES = Literal["xml", "json", "protobuf", "html", 0]


# @validate_call
def get_results(result_type: ALLOW_TYPES):
    allow_types = typing.get_args(ALLOW_TYPES)
    print(f"Allow types from Literal: {allow_types}")


UserID = NewType("UserID", int)
OrderID = NewType("OrderID", int)


def get_user_object_by_id(user_id: UserID):
    pass


if __name__ == "__main__":
    get_results(result_type=0)

    get_user_object_by_id(UserID(345))
    # get_user_object_by_id(345)
    # get_user_object_by_id(OrderID(123))
