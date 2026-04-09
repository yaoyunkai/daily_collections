"""
postgresql_usage.py

大小写敏感？
UTC / local time

python层 默认值 default
数据库层的 默认值 server_default


在 2.0 版本中，数据库的 NOT NULL 约束默认由 Python 的类型提示（Type Hint）决定。
    username: Mapped[str]
    nickname: Mapped[str | None]


============================================

inspection for table
1. psql tools: \d+ simple1;
2.
    SELECT
        column_name,
        data_type,
        character_maximum_length,
        column_default,
        is_nullable
    FROM
        information_schema.columns
    WHERE
        table_name = 'your_table_name';


created at 2026-04-09
"""

import enum
from datetime import datetime, timezone

import pendulum
from sqlalchemy import ARRAY, DateTime, Index, String, Text, create_engine, func, or_, select
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

engine = create_engine(
    "postgresql+psycopg://test1:test1@localhost:5432/demo1",
    connect_args={"options": "-c timezone=UTC"},
    echo=False,
)


class OrderStatus(enum.StrEnum):
    DRAFT = "S"  # 草稿 (Start )
    RUNNING = "R"  # 正在执行 (Running)
    DONE = "D"  # 已完成 (Done)


class Base(DeclarativeBase):
    pass


class Simple1(Base):
    __tablename__ = "simple1"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(Text)

    status: Mapped[OrderStatus] = mapped_column(
        String(1), default=OrderStatus.DRAFT, server_default=OrderStatus.DRAFT.value, nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    tags: Mapped[list[str]] = mapped_column(
        # 用 MutableList 包装 ARRAY，内部元素类型为 String(50)
        MutableList.as_mutable(ARRAY(String(20))),
        server_default="{}",
        nullable=False,
    )

    __table_args__ = (Index("idx_simple1_tags_gin", "tags", postgresql_using="gin"),)


def get_current_time():
    return pendulum.now()


def dt_from_database(obj: datetime):
    _obj = pendulum.instance(obj)
    return _obj.in_tz(pendulum.local_timezone())


def create_datetime_with_tz(year, month, day, hour, minute, second, *, tz=None):
    """
    创建带时区的时间，默认为UTC时区的时间

    """
    if tz is None:
        tz = timezone.utc

    return datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        tzinfo=tz,
    )


def create_demo_data():
    with Session(engine) as ss:
        obj1 = Simple1(name="Tom", content="xxxxxxxxxxxxxxxx1", created_at=get_current_time())
        obj2 = Simple1(name="tom", content="aaaaaaaaaaaaaaaaaaaa1")
        obj3 = Simple1(name="Peter", content="ccccccccccccccccccccccccccc", status=OrderStatus.DONE)
        obj4 = Simple1(
            name="David",
            content="DDDDDDDDDDDDDDDDDDDDDDDDDDDDDD",
            created_at=create_datetime_with_tz(2026, 4, 9, 11, 34, 44),
        )
        ss.add(obj1)
        ss.add(obj2)
        ss.add(obj3)
        ss.add(obj4)
        ss.commit()


def get_demo_data():
    with Session(engine) as ss:
        stmt = select(Simple1).where(Simple1.id == 1)
        obj1 = ss.scalar(stmt)
        dt_obj = dt_from_database(obj1.created_at)
        print(dt_obj)


def get_demo_data1():
    stmt = select(Simple1).where(or_(Simple1.name.like("_om"), Simple1.status == OrderStatus.DONE))
    with Session(engine) as ss:
        objs = ss.scalars(stmt)
        for obj in objs:
            dt_obj = dt_from_database(obj.created_at)
            print(dt_obj)


if __name__ == "__main__":
    # Base.metadata.create_all(engine)
    # get_utc_current()
    # get_demo_data1()
    create_demo_data()
