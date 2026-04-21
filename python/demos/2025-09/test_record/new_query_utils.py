"""
new_query_utils.py


get_test_record_by_sernum


created at 2026-04-15
"""

from datetime import date, datetime
from enum import Enum
from pprint import pprint
from typing import Annotated, Optional

import pendulum
from data_utils import ENGINE
from pydantic import BaseModel, BeforeValidator, ConfigDict, field_validator, model_validator
from QueryExpr.runner import QMode, parse_query
from sqlalchemy import Select, or_, select
from sqlalchemy.orm import Session
from test_record import PassFail, TestRecord

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


class YieldSearchIn(BaseModel):
    sernum: ParamQueryList = None
    uuttype: ParamQueryList = None
    test_machine: ParamQueryList = None
    test_area: ParamQueryList = None

    start_date: date
    end_date: date
    data_type: DataType = DataType.TEST

    view_type: ViewType = ViewType.NO_DATE


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

    def multi_search_test_record(self, search_params: dict, *, max_rows=MAX_LIMIT):
        validated_params = MultiSearchIn.model_validate(search_params)

        stmt = select(TestRecord)
        stmt = self._make_common_params_stmt(stmt, validated_params)

        passfail_conditions = [
            (validated_params.include_pass, PassFail.Pass),
            (validated_params.include_fail, PassFail.Fail),
            (validated_params.include_start, PassFail.Start),
        ]
        passfail_list = [pf_enum for is_included, pf_enum in passfail_conditions if is_included]

        stmt = stmt.where(TestRecord.passfail.in_(passfail_list)).order_by(TestRecord.record_time.asc()).limit(max_rows)

        rows = self.session.scalars(stmt).all()
        return [TestRecordOut.model_validate(row) for row in rows]

    @classmethod
    def _make_common_params_stmt(cls, stmt: "Select", search_object: MultiSearchIn | YieldSearchIn):
        common_query_list = ["sernum", "uuttype", "test_machine", "test_area"]

        for param_name in common_query_list:
            query_data_list: list[tuple[QMode, str]] = getattr(search_object, param_name)
            if not query_data_list:
                continue

            orm_filed_obj = getattr(TestRecord, param_name)

            _or_list = []
            for query_mode, query_str in query_data_list:
                if query_mode is QMode.Normal:
                    _or_list.append(orm_filed_obj == query_str)
                if query_mode is QMode.Pattern:
                    _or_list.append(orm_filed_obj.like(query_str))

            if len(_or_list) == 0:
                continue

            stmt = stmt.where(or_(*_or_list))
            _or_list.clear()

        start_date = search_object.start_date
        start_date = pendulum.datetime(start_date.year, start_date.month, start_date.day)
        end_date = search_object.end_date
        end_date = pendulum.datetime(end_date.year, end_date.month, end_date.day).add(days=1)

        stmt = stmt.where(
            TestRecord.record_time >= start_date,
            TestRecord.record_time < end_date,
        )

        if search_object.data_type is DataType.FIRST_PASS:
            stmt = stmt.where(TestRecord.first_pass_flag == True)  # noqa: E712

        return stmt


if __name__ == "__main__":
    query = Querying(ENGINE)
    param1 = {
        "sernum": " FCW%",
        "start_date": "2024-11-19",
        "end_date": "2024-11-20",
        "include_start": False,
        "data_type": "test",
    }

    ret = query.multi_search_test_record(param1)
    pprint(ret)
