"""

sernum       ^[a-zA-Z0-9-_]{3,35}$

pid          ^[a-zA-Z0-9-=+\\_\/|.]{3,40}$

uuttype      ^[a-zA-Z0-9-=+\\_\/|.]{3,40}$

test area    ^[a-zA-Z0-9_]{1,19}$

tan
^(?P<class_code>800|73|68|34|341|66|74|15|10|30|16|05|58|72)-
(?P<cisco_identifier>[0001-99999999999]{4,11})-(?P<version>[01-99]{2})$


https://docs.python.org/zh-cn/3.11/howto/enum.html


created at 2024/12/12
"""
from datetime import date
from enum import Enum, IntFlag
from typing import Optional

from pydantic import BaseModel, model_validator, ValidationError  # NOQA
from typing_extensions import Self


def is_blank(value: str):
    return value is None or value.strip() == ''


class DataType(Enum):
    """

    DataType('all')

    """

    ALL = 'all'
    FPY = 'first_pass_yield'
    BOARD = 'board_yield'


class PassFailFlag(IntFlag):
    Start = 0b100
    Fail = 0b010
    Pass = 0b001

    # Default = PassFailFlag.Pass | PassFailFlag.Fail
    Default = 0b011
    Null = 0b000
    All = 0b111


class MultiSearch(BaseModel):
    # support % _
    sernum: Optional[str] = None
    uuttype: Optional[str] = None
    machine: Optional[str] = None
    area: Optional[str] = None

    start_date: date
    end_date: date

    data_type: DataType = DataType.ALL
    passfail: int = PassFailFlag.Default

    select_start: bool = False
    select_pass: bool = True
    select_fail: bool = True

    test_container: Optional[str] = None
    test_user: Optional[str] = None

    @model_validator(mode='after')
    def check_model_fields(self) -> Self:
        if self.sernum is None and self.uuttype is None and self.machine is None and self.area is None:
            raise ValueError('sernum & uuttype & machine & area: cannot all be empty')

        if self.start_date > self.end_date:
            raise ValueError('start date must <= end date')

        return self


if __name__ == '__main__':
    data1 = dict(
        sernum='demo1',
        start_date='2024-12-10',
        end_date='2024-12-12',
        data_type='all',
        passfail=0b111,
    )

    MultiSearch.model_validate(data1)

    obj2 = PassFailFlag(0b111)
    print(obj2.__repr__())
    obj3 = PassFailFlag(0b101)
    print(obj3.__repr__())
