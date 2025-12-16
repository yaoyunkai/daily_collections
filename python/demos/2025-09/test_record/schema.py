"""
Test record tables

session.add
session.flush    将当前 Session 中所有挂起的变更（新增、修改、删除）发送到数据库，但暂时不提交事务。
session.commit

Identity Map

"""
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column

DATABASE_URL = "postgresql+psycopg2://test1:test1@localhost:5432/demo1"
engine = create_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass


class Demo1(Base):
    __tablename__ = 'demo1'
    id: Mapped[int] = mapped_column(primary_key=True)
    x: Mapped[int] = mapped_column(default=0)
    y: Mapped[int] = mapped_column(default=0)


class TestRecord(Base):
    """
    first_pass_flag: -1  means unset
                      0  means not first pass
                      1  means first pass

    passfail:           P pass
                        F fail
                        S start
                        A sampling

    """
    __tablename__ = 'test_record'
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    first_pass_flag: Mapped[int] = mapped_column(Integer, server_default=text('-1'))

    tst_id: Mapped[str] = mapped_column(String(30))
    record_time: Mapped[datetime] = mapped_column(DateTime)
    sernum: Mapped[str] = mapped_column(String(50))
    uuttype: Mapped[str] = mapped_column(String(50))
    test_area: Mapped[str] = mapped_column(String(20))
    passfail: Mapped[str] = mapped_column(String(5))
    runtime: Mapped[int] = mapped_column(Integer, server_default=text('0'))
    test_fail: Mapped[str] = mapped_column(String(50))
    test_machine: Mapped[str] = mapped_column(String(20))
    test_container: Mapped[str] = mapped_column(String(50))
    test_mode: Mapped[str] = mapped_column(String(10), server_default=text("'PROD0'"))
    deviation: Mapped[str] = mapped_column(String(16))

    testr1name: Mapped[str] = mapped_column(String(50))
    testr1: Mapped[str] = mapped_column(String(50))
    testr2name: Mapped[str] = mapped_column(String(50))
    testr2: Mapped[str] = mapped_column(String(50))
    testr3name: Mapped[str] = mapped_column(String(50))
    testr3: Mapped[str] = mapped_column(String(50))


def create_tables():
    Base.metadata.create_all(engine)


def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            print("连接成功！数据库版本:")
            print(result.scalar())
    except Exception as e:
        print(f"连接失败: {e}")


def test_demo1():
    with Session(engine) as session:
        p1 = Demo1(x=3, y=4)
        p2 = Demo1(x=5, y=7)
        session.add(p1)
        session.add(p2)
        session.commit()
        print(p1.id)
        print(p2.id)
        session.delete(p1)
        session.delete(p2)
        session.commit()


if __name__ == '__main__':
    # test_demo1()
    # create_tables()
    test_connection()
