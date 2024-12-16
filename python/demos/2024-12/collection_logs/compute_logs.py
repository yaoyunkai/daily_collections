"""
处理 iphone log

日期匹配: (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s{1,2}\d{1,2} \d{2}:\d{2}:\d{2}
设备名称: iPhone
进程匹配:  [a-zA-Z()]+\[\d+\]

\w+\[\d+\]

kernel()[0]
wifip2pd[195]
wifid(WiFiPolicy)[50]

日志级别: <[a-zA-Z]+>

结尾:   :

Nov 30 16:47:45


"""
import datetime
import re

from sqlalchemy import String, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import mapped_column, Mapped

LOG_PATH1 = "20241130_164806_117_iPhone.log"
ONE_MB = 1024 * 1024 * 1024
MONTH_DESC = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
YEAR = 2024

PATTERN_LOG = re.compile(
    r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s{1,2}\d{1,2} \d{2}:\d{2}:\d{2}) '
    r'iPhone ([a-zA-Z0-9().\-_]+)\[\d+\] <([a-zA-Z]+)>: '
)

engine = create_engine("mysql+mysqldb://root:password@localhost/sql_adv",
                       pool_recycle=3600, echo=True)


class Base(DeclarativeBase):
    pass


class Logs(Base):
    __tablename__ = 'logs'
    id: Mapped[int] = mapped_column(primary_key=True)
    log_date: Mapped[datetime.datetime]
    log_process: Mapped[str] = mapped_column(String(100))
    log_level: Mapped[str] = mapped_column(String(16))
    log_msg: Mapped[str] = mapped_column(Text, nullable=False)


def to_datetime(val: str):
    _hour = int(val[-8:-6])
    _minute = int(val[-5:-3])
    _second = int(val[-2:])
    _day = int(val.split()[1])
    _month = MONTH_DESC.index(val.split()[0]) + 1

    return datetime.datetime(
        year=YEAR, month=_month, day=_day,
        hour=_hour, minute=_minute, second=_second
    )


def collect_logs(log_path=None, saved=False):
    if not log_path:
        log_path = LOG_PATH1
    with open(log_path, mode='r', encoding='utf8') as fp:
        content = fp.read()

    content = str.replace(content, '\n', '')
    total_results = []

    start_pos = 0

    while True:
        match_res = PATTERN_LOG.search(content, start_pos)
        if not match_res:
            print('nothing to do')
            break

        end_pos = match_res.end()
        log_datetime, log_process, log_level = match_res.groups()
        log_datetime = to_datetime(log_datetime)

        # search next item
        next_match_res = PATTERN_LOG.search(content, end_pos)
        if next_match_res:
            next_start_pos = next_match_res.start()
            log_content = content[end_pos: next_start_pos]
            total_results.append([log_datetime, log_process, log_level, log_content])
            start_pos = next_start_pos

        else:
            log_content = content[end_pos:]
            total_results.append([log_datetime, log_process, log_level, log_content])
            break

    print(f'get {len(total_results)} logs')

    if not saved:
        return

    orm_objs = []

    for item in total_results:
        orm_objs.append(
            Logs(log_date=item[0], log_process=item[1], log_level=item[2], log_msg=item[3])
        )

    with Session(engine) as session:
        session.add_all(orm_objs)
        session.commit()


if __name__ == '__main__':
    collect_logs(saved=False)
