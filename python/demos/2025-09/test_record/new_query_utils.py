"""
new_query_utils.py


get_test_record_by_sernum


created at 2026-04-15
"""

from datetime import date
from enum import Enum
from typing import Optional

from data_utils import ENGINE
from pydantic import BaseModel
from QueryExpr.runner import parse_query
from sqlalchemy import select
from sqlalchemy.orm import Session
from test_record import TestRecord

MAX_LIMIT = 5000


class DataType(Enum):
    TEST = "test"
    FIRST_PASS = "first_pass"


class ViewType(Enum):
    NO_DATE = "no_date"
    WEEK = "week"
    MONTH = "month"


class MultiSearchParams(BaseModel):
    sernum: Optional[str] = None
    uuttype: Optional[str] = None
    test_machine: Optional[str] = None
    test_area: Optional[str] = None

    start_date: date
    end_date: date

    data_type: DataType = DataType.TEST

    # must select one of below include_
    include_pass: bool = True
    include_fail: bool = True
    include_start: bool = True


class Querying(object):
    def __init__(self, engine):
        self.session = Session(engine)

    def get_test_record_by_sernum(self, sernum: str):
        stmt = select(TestRecord).where(TestRecord.sernum == sernum).order_by(TestRecord.record_time.asc())
        return self.session.scalars(stmt).all()


if __name__ == "__main__":
    query = Querying(ENGINE)
    ret = parse_query("IE-3500-8P2S-E,IEM-3500-16P=")
    print(ret)
