"""

sernum       ^[a-zA-Z0-9-_]{3,35}$

pid          ^[a-zA-Z0-9-=+\\_\/|.]{3,40}$

uuttype      ^[a-zA-Z0-9-=+\\_\/|.]{3,40}$

test area    ^[a-zA-Z0-9_]{1,19}$

tan
^(?P<class_code>800|73|68|34|341|66|74|15|10|30|16|05|58|72)-
(?P<cisco_identifier>[0001-99999999999]{4,11})-(?P<version>[01-99]{2})$


https://docs.python.org/zh-cn/3.11/howto/enum.html

Enum:
    name
    value

初始化方式  Enum['name']  Enum(value)


created at 2024/12/12
"""
import re
from datetime import date, datetime
from enum import Enum, IntFlag, auto
from functools import partial
from re import Pattern
from typing import Optional, Self

from pydantic import BaseModel, model_validator, ValidationError, ConfigDict  # NOQA

SEPARATOR = ','

PATTERN_SERNUM = re.compile(r'^[a-zA-Z0-9-_]{3,35}$')
PATTERN_PID = re.compile(r'^[a-zA-Z0-9-=+\\_/|.]{3,40}$')
PATTERN_AREA = re.compile(r'^[a-zA-Z0-9_]{1,19}$')
PATTERN_MACHINE = re.compile(r'^[a-z0-9]{5,20}$')


class ParamType(Enum):
    Normal = auto()
    FuzzyQ = auto()


Param = tuple[str, ParamType]


def is_blank(value: str):
    return value is None or value.strip() == ''


def get_params_from_value(value: str, param_pattern: Pattern) -> list[Param]:
    results = []

    # because value may be null
    if is_blank(value):
        return results

    if SEPARATOR in value:
        value = [_inner.strip() for _inner in value.split(SEPARATOR)]
    else:
        value = [value, ]

    for param_item in value:
        if is_blank(param_item):
            continue

        param_type = ParamType.Normal
        to_check = param_item

        if '%' in param_item:
            param_type = ParamType.FuzzyQ
            to_check = param_item.replace('%', '')

        if not param_pattern.match(to_check):
            continue

        results.append((param_item, param_type))

    return results


get_params_from_sernum = partial(get_params_from_value, param_pattern=PATTERN_SERNUM)
get_params_from_uuttype = partial(get_params_from_value, param_pattern=PATTERN_PID)
get_params_from_machine = partial(get_params_from_value, param_pattern=PATTERN_MACHINE)
get_params_from_area = partial(get_params_from_value, param_pattern=PATTERN_AREA)

FUNC_MAP = {
    'sernum': get_params_from_sernum,
    'uuttype': get_params_from_uuttype,
    'machine': get_params_from_machine,
    'area': get_params_from_area,
}


class DataType(Enum):
    """

    DataType('all')

    """

    FPY = 'first_pass_yield'
    BOARD = 'board_yield'
    TEST = 'test_yield'  # default is test yield


class ViewType(Enum):
    NoDate = 'no_date'
    Week = 'week'
    Month = 'month'


class PassFailFlag(IntFlag):
    Start = 0b100
    Fail = 0b010
    Pass = 0b001

    # Default = PassFailFlag.Pass | PassFailFlag.Fail
    # Null = 0b000
    # All = 0b111

    @classmethod
    def check_passfail_flag(cls, val):
        return 0b000 < val <= (cls.Start | cls.Pass | cls.Fail)

    @staticmethod
    def is_flag_set(flag: int, val: int):
        return (flag & val) == flag


class PyTestRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    record_time: datetime
    sernum: str
    uuttype: str
    area: str
    passfail: str
    run_time: int = 0
    test_failure: str = ''
    machine: str
    test_container: str
    test_user: str
    test_mode: str
    deviation: str
    bf_status: bool


class YieldParams(BaseModel):
    # support %
    sernum: Optional[str] = None
    uuttype: Optional[str] = None
    machine: Optional[str] = None
    area: Optional[str] = None

    start_date: date
    end_date: date

    view_type: ViewType = ViewType.NoDate
    yield_type: DataType = DataType.FPY

    @model_validator(mode='after')
    def check_model_fields(self) -> Self:
        if is_blank(self.sernum) and is_blank(self.uuttype) and is_blank(self.machine) and is_blank(self.area):
            raise ValueError('sernum & uuttype & machine & area: cannot all be empty')

        if self.start_date > self.end_date:
            raise ValueError('start date must <= end date')

        return self


class MultiSearchParams(BaseModel):
    # support %
    sernum: Optional[str] = None
    uuttype: Optional[str] = None
    machine: Optional[str] = None
    area: Optional[str] = None

    start_date: date
    end_date: date

    data_type: DataType = DataType.TEST
    passfail: PassFailFlag = PassFailFlag.Pass | PassFailFlag.Fail

    select_start: bool = False
    select_pass: bool = True
    select_fail: bool = True

    test_container: Optional[str] = None
    test_user: Optional[str] = None

    @model_validator(mode='after')
    def check_model_fields(self) -> Self:
        if is_blank(self.sernum) and is_blank(self.uuttype) and is_blank(self.machine) and is_blank(self.area):
            raise ValueError('sernum & uuttype & machine & area: cannot all be empty')

        if self.start_date > self.end_date:
            raise ValueError('start date must <= end date')

        if not PassFailFlag.check_passfail_flag(self.passfail):
            raise ValueError('passfail not in range')

        return self


if __name__ == '__main__':
    data1 = dict(
        sernum='demo1',
        start_date='2024-12-10',
        end_date='2024-12-12',
        data_type=DataType.TEST,
        passfail=PassFailFlag.Fail,
    )

    obj1 = MultiSearchParams.model_validate(data1)
    # print(obj1.passfail)
    # print(obj1.passfail.__repr__())
    #
    # obj2 = PassFailFlag(0b111)
    # for item in obj2:
    #     print(item.__repr__())

    print(get_params_from_uuttype('IEM-3400, IEM-3400-%, IE-3000, IE-4500-%,'))
    print(get_params_from_uuttype('IE-34550,'))
