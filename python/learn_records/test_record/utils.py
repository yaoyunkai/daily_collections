"""



created at 2024/12/12
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MultiSearch(BaseModel):
    # support % _
    sernum: Optional[str]
    uuttype: Optional[str]
    machine: Optional[str]
    area: Optional[str]

    start_date: datetime
    end_date: datetime

    data_type: str  # first_pass, test
    passfail: str  # F P S

    test_container: Optional[str]
    test_user: Optional[str]


if __name__ == '__main__':
    # demo_obj = MultiSearch(sernum='s')
    pass
