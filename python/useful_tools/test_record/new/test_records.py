"""


Created at 2023/12/25
"""
import enum

from sqlalchemy import create_engine
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.ddl import CreateTable

url = 'mysql+mysqldb://root:password@localhost:3306/sql_adv?charset=utf8'
engine = create_engine(url, pool_recycle=3600, echo=True)


class Base(DeclarativeBase):
    pass


class TestResultEnum(enum.Enum):
    PASS = 'P'
    FAIL = 'F'
    START = 'S'
    SAMPLING = 'A'


class TestRecord(Base):
    __tablename__ = 'test_record'

    id: Mapped[int] = mapped_column(primary_key=True)


def show_test_record_ddl():
    print(CreateTable(TestRecord.__table__).compile(dialect=mysql.dialect()))


if __name__ == '__main__':
    show_test_record_ddl()
