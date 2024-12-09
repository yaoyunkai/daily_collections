"""
Base.metadata.create_all(engine)

session.flush()

created at 2024/12/9
"""

import json
import re
from datetime import datetime

from sqlalchemy import String, CHAR, Integer, Boolean, TIMESTAMP, func
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Session

url = 'mysql+mysqldb://root:password@localhost:3306/sql_adv?charset=utf8'
engine = create_engine(url, echo=True)


def convert_datetime(val: str):
    pattern = re.compile(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})')
    matched = pattern.search(val)
    if not matched:
        raise ValueError

    return datetime(*[int(i) for i in matched.groups()])


class Base(DeclarativeBase):
    pass


class TestRecord(Base):
    """
    bfstatus

    """
    __tablename__ = "test_record"

    id: Mapped[int] = mapped_column(primary_key=True)

    record_time: Mapped[datetime]
    sernum: Mapped[str] = mapped_column(String(50))  # upper
    uuttype: Mapped[str] = mapped_column(String(50))  # upper
    area: Mapped[str] = mapped_column(String(20))  # upper
    passfail: Mapped[str] = mapped_column(CHAR(1))  # S: Start A: ADT Sampling P: Passed F: Failed
    run_time: Mapped[int] = mapped_column(Integer, default=0)  # unit: seconds
    test_failure: Mapped[str] = mapped_column(String(60))  # default should be ""
    machine: Mapped[str] = mapped_column(String(20))  # lower

    test_container: Mapped[str] = mapped_column(String(50))  # not none
    test_user: Mapped[str] = mapped_column(String(40), default='')
    test_mode: Mapped[str] = mapped_column(CHAR(5), default='PROD0')  # default is PROD0, DEBUG
    deviation: Mapped[str] = mapped_column(String(35), default='D000000')
    bf_status: Mapped[bool] = mapped_column(Boolean, default=False)  # backflush status

    create_time: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    first_pass: Mapped[str] = mapped_column(CHAR(1), server_default='N')  # N == None, T == True, F == False


Base.metadata.create_all(engine)


def load_data_from_json(filename: str):
    data = json.load(open(filename))
    data = data['results']['data']

    session = Session(engine)
    cnt = 0

    for item in data:
        cnt += 1

        tr_obj = TestRecord()
        tr_obj.record_time = convert_datetime(item['rectime'])
        tr_obj.sernum = item['sernum']
        tr_obj.uuttype = item['uuttype']
        tr_obj.area = item['area']
        tr_obj.passfail = item['passfail']
        tr_obj.run_time = item['attributes'].get('RUNTIME', 0)
        tr_obj.test_failure = item['attributes'].get('TEST', '')
        tr_obj.machine = item['machine']
        tr_obj.test_container = item['attributes'].get('CONTAINER', '')
        tr_obj.test_user = item['attributes'].get('USERNAME', '')
        tr_obj.deviation = item['attributes'].get('DEVIATION', 'D000000')
        tr_obj.bf_status = True if item.get('bfstatus') == 'YES' else False

        tr_obj.first_pass = 'N'
        # op(t_obj)

        session.add(tr_obj)
        if cnt % 100 == 0:
            session.flush()

    session.commit()


if __name__ == '__main__':
    pass
