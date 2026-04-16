"""
new_query_utils.py


get_test_record_by_sernum


created at 2026-04-15
"""

from data_utils import ENGINE
from QueryExpr.runner import parse_query
from sqlalchemy import select
from sqlalchemy.orm import Session
from test_record import TestRecord


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
