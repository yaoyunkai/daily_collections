"""

sernum       ^[a-zA-Z0-9-_]{3,35}$

pid          ^[a-zA-Z0-9-=+\\_\/|.]{3,40}$

uuttype      ^[a-zA-Z0-9-=+\\_\/|.]{3,40}$

test area    ^[a-zA-Z0-9_]{1,19}$

tan
^(?P<class_code>800|73|68|34|341|66|74|15|10|30|16|05|58|72)-
(?P<cisco_identifier>[0001-99999999999]{4,11})-(?P<version>[01-99]{2})$



created at 2024/12/12
"""
from datetime import date
from typing import Optional

from pydantic import BaseModel, model_validator, ValidationError  # NOQA
from typing_extensions import Self


def validate_filed(value: str):
    """
    % _  模式匹配

    , for split each item

    """

    pass


class MultiSearch(BaseModel):
    # support % _
    sernum: Optional[str] = None
    uuttype: Optional[str] = None
    machine: Optional[str] = None
    area: Optional[str] = None

    start_date: date
    end_date: date

    data_type: str  # first_pass, test
    passfail: str  # F P S

    test_container: Optional[str] = None
    test_user: Optional[str] = None

    @model_validator(mode='after')
    def check_all_blanks(self) -> Self:
        if self.sernum is None and self.uuttype is None and self.machine is None and self.area is None:
            raise ValueError('sernum & uuttype & machine & area: cannot all be empty')

        return self


if __name__ == '__main__':
    # demo_obj = MultiSearch(sernum='s')
    data1 = dict(
        sernum='12345',
        start_date='2020-10-01',
        end_date='2020-10-01',
        data_type='sss',
        passfail='123'
    )

    obj1 = MultiSearch.model_validate(data1)

    print(obj1.start_date)
    print(type(obj1.start_date))
