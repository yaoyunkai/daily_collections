"""
query utils

"""
import enum
from datetime import date
from datetime import datetime
from typing import Optional
from typing import Self

from dateutil.relativedelta import relativedelta
from objprint import op
from pydantic import BaseModel
from pydantic import model_validator
from sqlalchemy import asc
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy.orm import Session

import schema
from schema import TestRecord

SEPARATOR = ','


def is_blank(value: str):
    return value is None or value.strip() == ''


def get_current_and_last_month_dates() -> tuple[date, date]:
    current_date = date.today()
    one_month_ago_date = current_date - relativedelta(months=1)
    return current_date, one_month_ago_date


def date_to_datetime(date_obj: date) -> datetime:
    return datetime(date_obj.year, date_obj.month, date_obj.day)


def parse_params_from_string(value: str):
    structured_data = []
    items = [item.strip() for item in value.split(SEPARATOR)]
    for item in items:
        if not item:
            continue
        if '%' in item or '_' in item:
            structured_data.append((QueryParamType.PATTERN, item))
        else:
            structured_data.append((QueryParamType.NORMAL, item))
    return structured_data


class QueryParamType(enum.StrEnum):
    NORMAL = 'N'
    PATTERN = 'P'


class PassFailType(enum.StrEnum):
    PASS = 'P'
    FAIL = 'F'
    START = 'S'
    SAMPLING = 'A'


class DataType(enum.StrEnum):
    TEST = 'test'
    FIRST_PASS = 'first_pass'


class ViewType(enum.StrEnum):
    NO_DATE = 'no_date'
    WEEK = 'week'
    MONTH = 'month'


class MultiSearchParams(BaseModel):
    sernum: Optional[str] = None
    uuttype: Optional[str] = None
    test_machine: Optional[str] = None
    test_area: Optional[str] = None

    start_date: date
    end_date: date

    data_type: DataType = DataType.TEST
    passfail: str

    @model_validator(mode='after')
    def check_model_fields(self) -> Self:
        if (is_blank(self.sernum) and is_blank(self.uuttype) and
                is_blank(self.test_machine) and is_blank(self.test_area)):
            raise ValueError('sernum & uuttype & test_machine & test_area: cannot all be empty')

        if self.start_date > self.end_date:
            raise ValueError('start date must <= end date')

        return self

    def get_passfail_flags(self):
        _ret = []
        if PassFailType.PASS in self.passfail:
            _ret.append(PassFailType.PASS.value)
        if PassFailType.FAIL in self.passfail:
            _ret.append(PassFailType.FAIL.value)
        if PassFailType.START in self.passfail:
            _ret.append(PassFailType.START.value)
        if PassFailType.SAMPLING in self.passfail:
            _ret.append(PassFailType.SAMPLING.value)
        if not _ret:
            raise ValueError('invalid passfail value')
        return _ret


class YieldParams(BaseModel):
    # support %
    sernum: Optional[str] = None
    uuttype: Optional[str] = None
    test_machine: Optional[str] = None
    test_area: Optional[str] = None

    start_date: date
    end_date: date

    view_type: ViewType = ViewType.NO_DATE
    yield_type: DataType = DataType.TEST

    @model_validator(mode='after')
    def check_model_fields(self) -> Self:
        if (is_blank(self.sernum) and is_blank(self.uuttype) and
                is_blank(self.test_machine) and is_blank(self.test_area)):
            raise ValueError('sernum & uuttype & test_machine & test_area: cannot all be empty')

        if self.start_date > self.end_date:
            raise ValueError('start date must <= end date')

        return self


def get_test_record_by_sernum(sernum):
    session = Session(schema.engine)

    _sql = (
        select(TestRecord).
        where(TestRecord.sernum == sernum).
        order_by(asc(TestRecord.record_time))
    )
    _result = []

    dataset = session.scalars(_sql).all()
    for item in dataset:
        op(item)
        _result.append(item)
    return _result


def _get_part_of_where_conditions(condition_list, m_obj):
    for field_name in ['sernum', 'uuttype', 'test_machine', 'test_area']:
        m_obj_attr = getattr(m_obj, field_name)
        if not m_obj_attr:
            continue

        field_obj = getattr(TestRecord, field_name)
        structured_params = parse_params_from_string(m_obj_attr)

        param_values = []
        for param_type, param_value in structured_params:
            if param_type == QueryParamType.NORMAL:
                param_values.append(field_obj == param_value)
            if param_type == QueryParamType.PATTERN:
                param_values.append(field_obj.like(param_value))

        if not param_values:
            continue
        if len(param_values) == 1:
            condition_list.append(param_values[0])
        else:
            condition_list.append(or_(*param_values))
        param_values.clear()

    start_datetime = date_to_datetime(m_obj.start_date)
    end_datetime = date_to_datetime(m_obj.end_date) + relativedelta(seconds=24 * 60 * 60 - 1)

    condition_list.append(
        TestRecord.record_time.between(start_datetime, end_datetime)
    )


def get_test_record_by_multisearch(value_dict):
    session = Session(schema.engine)

    try:
        m_obj = MultiSearchParams.model_validate(value_dict)
        passfail_flags = m_obj.get_passfail_flags()
    except Exception as e:
        raise schema.ParamException(e)

    stmt_where_conditions = []
    _get_part_of_where_conditions(stmt_where_conditions, m_obj)

    # there is issue, when first_pass_flag is unset -1,
    # some rows won't be detected., even if the row is first pass flag
    if m_obj.data_type == DataType.FIRST_PASS:
        stmt_where_conditions.append(
            TestRecord.first_pass_flag == schema.FirstPassState.FIRST
        )

    stmt_where_conditions.append(
        TestRecord.passfail.in_(passfail_flags)
    )

    dataset = session.scalars(
        select(TestRecord).
        where(*stmt_where_conditions).
        order_by(asc(TestRecord.record_time))
    ).all()
    for row in dataset:
        op(row)
    return dataset


def get_test_yield(value_dict: dict):
    session = Session(schema.engine)

    try:
        m_obj = YieldParams.model_validate(value_dict)
    except Exception as e:
        raise schema.ParamException(e)

    stmt_where_conditions = []
    _get_part_of_where_conditions(stmt_where_conditions, m_obj)

    # ADT sampling data need include ?
    stmt_where_conditions.append(
        TestRecord.passfail.in_(['P', 'F'])
    )

    if m_obj.yield_type == DataType.FIRST_PASS:
        stmt_where_conditions.append(
            TestRecord.first_pass_flag == schema.FirstPassState.FIRST
        )

    dataset = session.execute(
        select(
            TestRecord.record_time,
            TestRecord.sernum,
            TestRecord.uuttype,
            TestRecord.test_area,
            TestRecord.passfail,
            TestRecord.test_machine,
        ).where(*stmt_where_conditions)
    )
    for row in dataset:
        op(row)
    return dataset


if __name__ == '__main__':
    _query = {
        'uuttype': 'IE-3500-%',
        'start_date': '2024-11-20',
        'end_date': '2024-12-29',
        'view_type': ViewType.NO_DATE,
        'yield_type': DataType.TEST,
    }
    get_test_yield(_query)
