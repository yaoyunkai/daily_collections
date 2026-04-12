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
1. psql tools: \\d+ simple1;
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

from datetime import date, datetime
from enum import StrEnum
from pprint import pprint
from typing import Optional, Sequence

import pendulum
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, asc, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

engine = create_engine(
    "postgresql+psycopg://test1:test1@localhost:5432/demo1",
    connect_args={"options": "-c timezone=UTC", "connect_timeout": 3},
    echo=True,
)


class PostStatus(StrEnum):
    Draft = "S"
    ToReview = "T"
    Done = "D"


class GenderType(StrEnum):
    Unknown = "N"
    Man = "M"
    Woman = "W"


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50, "en-US-x-icu"), nullable=False)
    gender: Mapped[GenderType] = mapped_column(
        String(1),
        nullable=False,
        default=GenderType.Unknown,
        server_default=GenderType.Unknown.value,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(True), nullable=False, server_default=func.now())
    birthday: Mapped[Optional[date]] = mapped_column(Date)

    # posts: Mapped[list["Posts"]] = relationship("Posts", back_populates="person")


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"))
    title: Mapped[str] = mapped_column(String(100, "zh-Hans-CN-x-icu"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[PostStatus] = mapped_column(
        String(1),
        nullable=False,
        default=PostStatus.Draft,
        server_default=PostStatus.Draft.value,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(True), nullable=False, server_default=func.now())

    # person: Mapped["Person"] = relationship("Person", back_populates="posts")


def get_current_time():
    return pendulum.now()


def create_demo_persons():
    with Session(engine) as session:
        obj1 = Person(name="Tom", gender=GenderType.Man, birthday=date(2001, 4, 6))
        obj2 = Person(name="Peter", gender=GenderType.Man, birthday=date(1997, 3, 3))
        obj3 = Person(name="Lily", gender=GenderType.Woman, birthday=date(1989, 6, 23))
        session.add_all([obj1, obj2, obj3])
        session.commit()


def get_all_person():
    stmt = select(Person).order_by(asc(Person.name))

    with Session(engine) as session:
        for row in session.scalars(stmt):
            pprint(row.name)
            # pprint(row.posts)


def get_posts_by_person(person_id: int | Person) -> Sequence["Posts"]:
    target_id = person_id.id if isinstance(person_id, Person) else person_id
    stmt = select(Posts).where(Posts.person_id == target_id)
    with Session(engine) as session:
        return session.scalars(stmt).all()


if __name__ == "__main__":
    # create_demo_persons()
    get_all_person()
