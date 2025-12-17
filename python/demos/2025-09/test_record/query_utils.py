"""
query utils

"""
from objprint import op
from sqlalchemy import asc
from sqlalchemy import select
from sqlalchemy.orm import Session

import schema
from schema import TestRecord


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


if __name__ == '__main__':
    pass
