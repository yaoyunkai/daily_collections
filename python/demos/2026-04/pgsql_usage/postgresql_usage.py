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

import re
from datetime import date
from pprint import pprint
from typing import Sequence

import pendulum
from sqlalchemy import asc, create_engine, desc, func, select, text
from sqlalchemy.orm import Session
from tables import DummyArticle, GenderType, Person, Post, PostStatus

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


def get_all_articles(session: Session):
    stmt = select(DummyArticle).order_by(DummyArticle.id.desc())
    return session.scalars(stmt).all()


def get_post_count_by_person(session: Session, person_id: int) -> int:
    stmt = select(func.count(Post.id)).where(Post.person_id == person_id)
    return session.scalar(stmt) or 0


def get_draft_posts_last_two_months(session: Session) -> Sequence[Post]:
    stmt = select(Post).where(
        Post.status == PostStatus.Draft,
        Post.created_at >= text("NOW() - INTERVAL '2 months'"),
    )
    return session.scalars(stmt).all()


def get_person_ids_with_most_posts(session: Session) -> list[int]:
    # 1. 构建 CTE：统计每个人的文章数并计算排名 (rnk)
    cte = (
        select(
            Person.id.label("person_id"),
            # 使用 rank() 窗口函数处理并列第一的情况
            func.rank().over(order_by=func.count(Post.id).desc()).label("rnk"),
        )
        .outerjoin(Person.post)
        .group_by(Person.id)
        .cte("ranked_persons")
    )

    # 2. 主查询：直接从 CTE 中查出排名第一 (rnk == 1) 的 person_id
    stmt = select(cte.c.person_id).where(cte.c.rnk == 1)

    # session.scalars() 专门用于提取单列结果，.all() 将其转换为普通的 Python 列表 (例如: [1, 3, 5])
    return list(session.scalars(stmt).all())


def get_person_with_latest_draft(session: Session) -> Person | None:
    stmt = (
        select(Person)
        .join(Person.post)  # 关联 Post 表
        .where(Post.status == PostStatus.Draft)  # 筛选状态为草稿 (Draft) 的文章
        .order_by(Post.created_at.desc())  # 按文章创建时间降序排列 (最近的排在最前)
        .limit(1)  # 只取最新的一条
    )

    # session.scalar() 返回单个 Person 对象；如果没有草稿记录，则优雅地返回 None
    return session.scalar(stmt)


def update_article_content_and_tags(session: Session, article_id: int, new_content: str):
    """
    如果要使用 # , 需要转义 \#

    """
    article = session.get(DummyArticle, article_id)
    if not article:
        return None

    extracted_tags = re.findall(r"#(\w+)\s", new_content)

    article.content = new_content
    article.tags = list(set(extracted_tags))
    session.commit()
    return article


if __name__ == "__main__":
    """
    output something

    """
    # ret = get_all_articles(Session(engine))
    # print(ret)
