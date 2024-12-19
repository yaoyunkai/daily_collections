"""



created at 2024/12/12
"""
from datetime import date
from typing import Optional

from pydantic import BaseModel, model_validator, ValidationError  # NOQA
from typing_extensions import Self


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
        start_date='2020-10-01',
        end_date='2020-10-01',
        data_type='sss',
        passfail='123'
    )

    obj1 = MultiSearch.model_validate(data1)
