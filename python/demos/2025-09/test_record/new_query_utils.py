"""
new_query_utils.py


get_test_record_by_sernum


created at 2026-04-15
"""

from datetime import date, datetime
from enum import Enum
from typing import Annotated, Optional

from data_utils import ENGINE
from pydantic import BaseModel, BeforeValidator, ConfigDict, ValidationError, field_validator, model_validator
from QueryExpr.runner import QMode, parse_query
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


def _convert_param_str(param_str: str):
    return parse_query(param_str)


ParamQueryList = Annotated[Optional[list[tuple[QMode, str]]], BeforeValidator(_convert_param_str)]


class MultiSearchIn(BaseModel):
    sernum: ParamQueryList = None
    uuttype: ParamQueryList = None
    test_machine: ParamQueryList = None
    test_area: ParamQueryList = None

    start_date: date
    end_date: date

    data_type: DataType = DataType.TEST

    # must select one of below include_
    include_pass: bool = True
    include_fail: bool = True
    include_start: bool = True

    @model_validator(mode="after")
    def validate_cross_fields(self):
        if not any([self.sernum, self.uuttype, self.test_machine, self.test_area]):
            raise ValueError(
                "Must provide at least one search parameter: 'sernum', 'uuttype', 'test_machine', or 'test_area'."
            )

        if self.start_date > self.end_date:
            raise ValueError("'start_date' cannot be >= 'end_date'.")

        if not any([self.include_pass, self.include_fail, self.include_start]):
            raise ValueError("At least one of 'include_pass', 'include_fail', or 'include_start' must be True.")

        return self


class TestRecordOut(BaseModel):
    record_time: datetime
    sernum: str
    uuttype: str
    test_area: str
    passfail: str
    runtime: int
    test_fail: str
    test_machine: str
    test_container: str
    first_pass_flag: bool | None

    # 允许 Pydantic 从 SQLAlchemy 的 Row 或 ORM 对象中读取数据
    model_config = ConfigDict(from_attributes=True)

    @field_validator("passfail", mode="before")
    @classmethod
    def convert_passfail(cls, value) -> str:
        val_str = value.value if hasattr(value, "value") else str(value)
        mapping = {"pass": "P", "fail": "F", "start": "S"}
        return mapping.get(val_str.lower(), val_str)


class Querying(object):
    def __init__(self, engine):
        self.session = Session(engine)

    def get_test_record_by_sernum(self, sernum: str):
        stmt = (
            select(TestRecord)
            .where(TestRecord.sernum == sernum)
            .order_by(TestRecord.record_time.asc())
            .limit(MAX_LIMIT)
        )
        rows = self.session.scalars(stmt).all()

        return [TestRecordOut.model_validate(row) for row in rows]

    def multi_search_test_record(self, front_values: dict):
        try:
            search_data = MultiSearchIn.model_validate(front_values)
        except (ValidationError, ValueError):
            raise ValueError("invalid params")
        print(search_data)


if __name__ == "__main__":
    query = Querying(ENGINE)
    param1 = {
        "sernum": "FCW2846Y0QH",
        "start_date": "2025-01-01",
        "end_date": "2025-12-30",
        "include_start": False,
        "data_type": "test",
    }

    query.multi_search_test_record(param1)
