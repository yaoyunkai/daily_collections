"""
Base.metadata.create_all(engine)

session.flush()

created at 2024/12/9
"""

import json
import re
import time
from datetime import UTC, timedelta
from datetime import datetime
from pprint import pprint  # NOQA

from objprint import op  # NOQA
from sqlalchemy import String, CHAR, Integer, Boolean, TIMESTAMP, func
from sqlalchemy import create_engine
from sqlalchemy import or_  # NOQA
from sqlalchemy import select, asc, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Session

from utils import (
    MultiSearch, ParamType, DataType, PassFailFlag,
    get_params_from_sernum, get_params_from_uuttype,
    get_params_from_machine, get_params_from_area
)

no_arg = object()

func_map = {
    'sernum': get_params_from_sernum,
    'uuttype': get_params_from_uuttype,
    'machine': get_params_from_machine,
    'area': get_params_from_area,
}


class ParamException(Exception):
    pass


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


def datetime_to_str(val: datetime):
    return val.strftime('%Y-%m-%d %H:%M:%S')


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

    record_time: Mapped[datetime]  # UTC timezone
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


def check_sernum_area_exists(sernum: str, area: str, engine_session=None):
    """
    return True if exists

    """
    if engine_session is None:
        engine_session = get_db_connection()

    _sql = text("""
    select 1
    from test_record
    where first_pass != 'N'
      and sernum = :sernum
      and area = :area
    """)

    if isinstance(engine_session, Session):
        result = engine_session.execute(_sql, {'sernum': sernum, 'area': area})
        result = result.fetchone()
        return result is not None
    else:
        with engine_session.connect() as conn:
            result = conn.execute(_sql, {'sernum': sernum, 'area': area})
            result = result.fetchone()
            return result is not None


def compute_first_pass(engine=None):
    """
    1. get dataset , first_pass == 'N', and record time < current, order by record time.
    2. 检查是否为first_pass: a, 检查之前的 first_pass != N /  b, 检查当前的数据集。

    """
    print('start compute first pass')
    start_time = time.time()
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
    if len(dataset) == 0:
        print('no data need to compute first pass')
        return

    _sernum_area_set = set()

    for test_record in dataset:
        record_time = test_record.record_time
        sernum = test_record.sernum
        area = test_record.area
        sernum_area = '{}_{}'.format(sernum, area)

        record_exists = check_sernum_area_exists(sernum, area, session)

        if not record_exists and sernum_area not in _sernum_area_set:
            first_pass = True
        else:
            first_pass = False
        print(f'db record ({test_record.id}) "{record_time} {sernum} {area}" first_pass flag is {first_pass}')
        test_record.first_pass = 'T' if first_pass else 'F'
        _sernum_area_set.add(sernum_area)

        session.add(test_record)

    session.commit()
    print(f'finish compute first pass, cost {time.time() - start_time}s')


def get_test_record_by_sernum(sernum, engine=None):
    """
    check sernum format

    """
    if engine is None:
        engine = get_db_connection()

    session = Session(engine)

    _sql = (
        select(TestRecord).
        where(TestRecord.sernum == sernum).
        order_by(asc(TestRecord.record_time))
    )
    _result = []

    dataset = session.scalars(_sql)
    dataset = dataset.all()
    for item in dataset:
        _dict = dict()
        for k, v in item.__dict__.items():
            if not k.startswith('_') and k not in ['id', 'create_time', 'first_pass']:
                _dict[k] = v

            # convert datetime to string
            if isinstance(v, datetime):
                _dict[k] = datetime_to_str(v)

        _result.append(_dict)

    pprint(_result)
    return _result


def get_test_record(front_dict: dict, engine=None):
    if engine is None:
        engine = get_db_connection()

    session = Session(engine)

    try:
        m_obj = MultiSearch.model_validate(front_dict)
    except Exception as e:
        print(e)
        raise ParamException(e)

    # 1. 处理 sernum, uuttype, machine, area
    _sql_condition_list = []
    _param_list = []
    sernum_params = get_params_from_sernum(m_obj.sernum)
    if len(sernum_params) > 0:
        for param, param_type in sernum_params:
            if param_type is ParamType.Normal:
                _param_list.append(
                    TestRecord.sernum == param,
                )
            if param_type is ParamType.FuzzyQ:
                _param_list.append(
                    TestRecord.sernum.like(param),
                )
        _sql_condition_list.append(or_(*_param_list))
        _param_list.clear()

    uuttype_params = get_params_from_uuttype(m_obj.uuttype)
    if len(uuttype_params) > 0:
        for param, param_type in uuttype_params:
            if param_type is ParamType.Normal:
                _param_list.append(
                    TestRecord.uuttype == param,
                )
            if param_type is ParamType.FuzzyQ:
                _param_list.append(
                    TestRecord.uuttype.like(param),
                )
        _sql_condition_list.append(or_(*_param_list))
        _param_list.clear()

    machine_params = get_params_from_machine(m_obj.machine)
    if len(machine_params) > 0:
        for param, param_type in machine_params:
            if param_type is ParamType.Normal:
                _param_list.append(
                    TestRecord.machine == param,
                )
            if param_type is ParamType.FuzzyQ:
                _param_list.append(
                    TestRecord.machine.like(param),
                )
        _sql_condition_list.append(or_(*_param_list))
        _param_list.clear()

    area_params = get_params_from_area(m_obj.area)
    if len(area_params) > 0:
        for param, param_type in area_params:
            if param_type is ParamType.Normal:
                _param_list.append(
                    TestRecord.area == param,
                )
            if param_type is ParamType.FuzzyQ:
                _param_list.append(
                    TestRecord.area.like(param),
                )
        _sql_condition_list.append(or_(*_param_list))
        _param_list.clear()

    _sql_condition_list.append(
        TestRecord.record_time.between(
            m_obj.start_date,
            m_obj.end_date + timedelta(days=1)
        )
    )

    if m_obj.data_type is DataType.FPY:
        _sql_condition_list.append(
            TestRecord.first_pass == 'T'
        )

    _passfail = []
    if PassFailFlag.is_flag_set(PassFailFlag.Start, m_obj.passfail):
        _passfail.append('S')
    if PassFailFlag.is_flag_set(PassFailFlag.Fail, m_obj.passfail):
        _passfail.append('F')
    if PassFailFlag.is_flag_set(PassFailFlag.Pass, m_obj.passfail):
        _passfail.append('P')

    _sql_condition_list.append(
        TestRecord.passfail.in_(_passfail)
    )

    # 开始查询
    _final_results = []

    dataset = session.scalars(
        select(TestRecord).
        where(*_sql_condition_list).
        order_by(asc(TestRecord.record_time))
    )
    dataset = dataset.all()
    for item in dataset:
        _dict = dict()
        for k, v in item.__dict__.items():
            if not k.startswith('_') and k not in ['id', 'create_time', 'first_pass']:
                _dict[k] = v

            # convert datetime to string
            if isinstance(v, datetime):
                _dict[k] = datetime_to_str(v)

        _final_results.append(_dict)

    pprint(_final_results)
    return _final_results


if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    # compute_first_pass()
    data1 = dict(
        # sernum='',
        uuttype='IE-%,IEM-%',
        start_date='2024-11-20',
        end_date='2024-12-12',
        data_type='all',
        passfail=PassFailFlag.Fail | PassFailFlag.Pass,
    )
    get_test_record(data1)
