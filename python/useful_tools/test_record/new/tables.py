"""
Test record tables

sqlalchemy
fastapi
restframework
django ORM
MySQL

--------------------------------------

create table demo3.all_test_record
(
    tid          int auto_increment comment '数据库主键' primary key,
    tst_id       datetime    not null comment 'Test Id',
    record_time  datetime    not null comment 'test record time',
    sernum       varchar(40) not null comment '序列号',
    uuttype      varchar(40) not null comment 'UUTTYPE',
    test_area    varchar(20) not null comment '测试工站',
    test_result  char        not null comment '最终测试结果: S: Start A: ADT Sampling P: Passed F: Failed',
    run_time     int         not null comment '测试所用时间(单位:秒)',
    failure_item varchar(50) not null comment '测试failure item',
    machine      varchar(20) not null comment '测试服务器',
    container    varchar(40) not null comment '测试容器',
    test_user    varchar(35) not null comment '开始测试的用户/员工',
    test_mode    varchar(10) not null comment '测试模式: PROD: 生产模式 DEBUG: 调试模式',
    deviation    varchar(16) not null comment 'Deviation',
    testr1name   varchar(50) not null comment 'TE String Name 1',
    testr1       varchar(50) not null comment 'TE String 1',
    testr2name   varchar(50) not null comment 'TE String Name 2',
    testr2       varchar(50) not null comment 'TE String 2',
    testr3name   varchar(50) not null comment 'TE String Name 3',
    testr3       varchar(50) not null comment 'TE String 3'
)
    comment '测试记录';




"""
import json

from sqlalchemy import CHAR
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session

url = 'mysql+mysqldb://root:password@localhost:3306/demo3?charset=utf8'
engine = create_engine(url, pool_recycle=3600, echo=True)


class Base(DeclarativeBase):
    # customize the type mapping
    # type_annotation_map = {
    #     int: BIGINT,
    #     datetime: TIMESTAMP(timezone=True),
    #     str: String().with_variant(NVARCHAR, "mssql"),
    # }
    pass


class AllTestRecord(Base):
    __tablename__ = 'all_test_record'

    tid = Column(Integer, primary_key=True, autoincrement=True, comment='数据库主键')
    tst_id = Column(DateTime, nullable=False, comment='Test Id')
    record_time = Column(DateTime, nullable=False, comment='test record time')

    # upper start
    sernum = Column(String(40), nullable=False, comment='序列号')  # upper
    uuttype = Column(String(40), nullable=False, comment='UUTTYPE')  # upper
    test_area = Column(String(20), nullable=False, comment='测试工站')  # upper
    test_result = Column(CHAR(1), nullable=False, comment='最终测试结果: S: Start A: ADT Sampling P: Passed F: Failed')
    # upper end

    run_time = Column(Integer, nullable=False, comment='测试所用时间(单位:秒)')
    failure_item = Column(String(50), nullable=False, comment='测试failure item')  # upper
    machine = Column(String(20), nullable=False, comment='测试服务器')  # lower
    container = Column(String(40), nullable=False, comment='测试容器')
    test_user = Column(String(35), nullable=False, comment='开始测试的用户/员工')
    test_mode = Column(String(10), nullable=False, comment='测试模式: PROD: 生产模式 DEBUG: 调试模式')
    deviation = Column(String(16), nullable=False, comment='Deviation')
    testr1name = Column(String(60), nullable=False, comment='TE String Name 1')
    testr1 = Column(String(100), nullable=False, comment='TE String 1')
    testr2name = Column(String(60), nullable=False, comment='TE String Name 2')
    testr2 = Column(String(100), nullable=False, comment='TE String 2')
    testr3name = Column(String(60), nullable=False, comment='TE String Name 3')
    testr3 = Column(String(100), nullable=False, comment='TE String 3')


# Base.metadata.create_all(engine)


def convert_json_data(file_path):
    fp = open(file_path)
    root_data = json.load(fp)
    root_data = root_data['results']['data']

    _final_result = []

    for test_record in root_data:
        _item = dict()
        _item['tst_id'] = test_record['tst_id']
        _item['record_time'] = test_record['rectime']

        _item['sernum'] = test_record['sernum']
        _item['uuttype'] = test_record['uuttype']
        _item['test_area'] = test_record['area']
        _item['test_result'] = test_record['passfail']

        _item['run_time'] = test_record['attributes']['RUNTIME']
        _item['failure_item'] = test_record['attributes'].get('TEST', '')
        _item['machine'] = test_record['machine']
        _item['container'] = test_record['attributes']['CONTAINER']
        _item['test_user'] = test_record['attributes'].get('USERNAME', '')

        _item['test_mode'] = 'PROD0'
        _item['deviation'] = test_record['attributes']['DEVIATION']

        _item['testr1name'] = test_record['attributes'].get('TESTR1NAME', '')
        _item['testr1'] = test_record['attributes'].get('TESTR1', '')
        _item['testr2name'] = test_record['attributes'].get('TESTR2NAME', '')
        _item['testr2'] = test_record['attributes'].get('TESTR2', '')
        _item['testr3name'] = test_record['attributes'].get('TESTR3NAME', '')
        _item['testr3'] = test_record['attributes'].get('TESTR3', '')

        adt_flag = test_record['attributes'].get('ADT_ACTIVE_AREA')
        if adt_flag:
            continue
        _final_result.append(_item)
    return _final_result


def save_data_to_db():
    with Session(engine) as session:
        session.execute(insert(AllTestRecord), convert_json_data('data.json'))
        session.commit()


if __name__ == '__main__':
    # convert_json_data('data.json')
    # save_data_to_db()
    pass
