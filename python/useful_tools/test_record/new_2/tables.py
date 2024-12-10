"""
Base.metadata.create_all(engine)

session.flush()

created at 2024/12/9
"""

import json
import re
from datetime import UTC
from datetime import datetime

from sqlalchemy import String, CHAR, Integer, Boolean, TIMESTAMP, func
from sqlalchemy import create_engine
from sqlalchemy import select, asc
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Session


# logging.basicConfig(level=logging.DEBUG, format='%(message)s', stream=sys.stdout)
# logger = logging.getLogger(__name__)


def get_db_connection():
    url = 'mysql+mysqldb://root:password@localhost:3306/sql_adv?charset=utf8'
    engine = create_engine(url, echo=True)
    return engine


def convert_datetime(val: str):
    pattern = re.compile(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})')
    matched = pattern.search(val)
    if not matched:
        raise ValueError

    return datetime(*[int(i) for i in matched.groups()])


def pretty_output(number: int, unit: str):
    if number < 2:
        return f'{number} {unit}'
    else:
        return f'{number} {unit}s'


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


def load_data_from_json(filename: str, engine=None):
    data = json.load(open(filename))
    data = data['results']['data']

    if engine is None:
        engine = get_db_connection()

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


def compute_first_pass(engine=None):
    """
    1. get dataset , first_pass == 'N', and record time < current, order by record time.
    2. 检查是否为first_pass: a, 检查之前的 first_pass != N, 检查当前的数据集。

    """
    print('start compute first pass')
    if engine is None:
        engine = get_db_connection()

    cur_time = datetime.now(tz=UTC)
    session = Session(engine)

    dataset_sql = (
        select(TestRecord).
        where(TestRecord.first_pass == 'N', TestRecord.record_time < cur_time).
        order_by(asc(TestRecord.record_time))
    )
    dataset = session.scalars(dataset_sql).all()

    print('fetch {} from db'.format(pretty_output(len(dataset), 'row')))
    _sernum_area_set = set()

    for test_record in dataset:
        record_time = test_record.record_time
        sernum = test_record.sernum
        area = test_record.area
        print(f'{record_time} {sernum} {area}')


if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    compute_first_pass()
