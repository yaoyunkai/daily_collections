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

from datetime import date
from pprint import pprint
from typing import Sequence

import pendulum
from sqlalchemy import asc, create_engine, desc, func, select, text
from sqlalchemy.orm import Session
from tables import GenderType, Person, Post, PostStatus

engine = create_engine(
    "postgresql+psycopg://test1:test1@localhost:5432/demo1",
    connect_args={"options": "-c timezone=UTC", "connect_timeout": 3},
    echo=True,
)


def get_current_time():
    return pendulum.now()


def create_demo_persons():
    with Session(engine) as session:
        obj1 = Person(name="Tom", gender=GenderType.Man, birthday=date(2001, 4, 6))
        obj2 = Person(name="Peter", gender=GenderType.Man, birthday=date(1997, 3, 3))
        obj3 = Person(name="Lily", gender=GenderType.Woman, birthday=date(1989, 6, 23))
        session.add_all([obj1, obj2, obj3])
        session.commit()


def get_first_person_id_by_name(person_name: str, session: Session):
    stmt = select(Person.id).where(Person.name == person_name).order_by(desc(Person.created_at))
    return session.scalars(stmt).first()


def create_demo_posts():
    with Session(engine) as session:
        p_tom = get_first_person_id_by_name("Tom", session)
        p_peter = get_first_person_id_by_name("Peter", session)
        p_lily = get_first_person_id_by_name("Lily", session)

        if p_tom:
            post1 = Post(title="这是第一个标题", content="aaaaaaaaaaaaaaaaaaaaaaaaaaa", person_id=p_tom)
            post2 = Post(title="这是第二个标题", content="bbbbbbbbbbbbbbbbbbbbbbbbbbbbb", person_id=p_tom)
            session.add(post1)
            session.add(post2)

        if p_peter:
            post3 = Post(title="这是第3个标题", content="cccccccccccccc", person_id=p_peter)
            post4 = Post(title="这是第4个标题", content="ddddddddddd", person_id=p_peter)
            session.add(post3)
            session.add(post4)

        if p_lily:
            post5 = Post(title="这是第5个标题", content="eeeeeeeeeeeeeeeeeeeeeeeeeee", person_id=p_lily)
            post6 = Post(title="这是第6个标题", content="ffffffffffffffffffffffff", person_id=p_lily)
            session.add(post5)
            session.add(post6)

        session.commit()


def get_all_person():
    stmt = select(Person).order_by(asc(Person.name))

    with Session(engine) as session:
        for row in session.scalars(stmt):
            pprint(row.name)


def get_post_count(session: Session, person_id: int) -> int:
    stmt = select(func.count().label("post_count")).where(Post.person_id == person_id)
    return session.execute(stmt).scalar_one()


def get_recent_status_s_posts(session: Session) -> Sequence[Post]:
    stmt = (
        select(Post)
        .where(Post.status == PostStatus.Draft, Post.created_at >= text("now() - interval '2 months'"))
        .order_by(Post.created_at.desc())
    )
    return session.scalars(stmt).all()


if __name__ == "__main__":
    # create_demo_persons()
    # get_all_person()

    # ret = get_post_count(Session(engine), 5)
    # print(ret)

    # for row in get_recent_status_s_posts(Session(engine)):
    #     print(row)

    pass
