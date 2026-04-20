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

from pprint import pprint
from typing import Optional

import pendulum
from sqlalchemy import asc, create_engine, func, select
from sqlalchemy.orm import Session
from tables import Base, Person, Post, PostStatus

engine = create_engine(
    "postgresql+psycopg://test1:test1@localhost:5432/demo1",
    connect_args={"options": "-c timezone=UTC", "connect_timeout": 3},
    echo=True,
)


def create_tables(eng):
    Base.metadata.create_all(eng)


def get_current_time():
    return pendulum.now()


def get_all_person():
    stmt = select(Person).order_by(asc(Person.name))

    with Session(engine) as session:
        for row in session.scalars(stmt):
            pprint(row.name)


def get_person_by_id(session: Session, person_id: int) -> Optional[Person]:
    """
    根据 ID 查询 Person，如果不存在则返回 None。
    对应 SQL: SELECT * FROM person WHERE id = :person_id;
    """
    return session.get(Person, person_id)


def get_persons_with_most_done_posts(session: Session) -> list[Person]:
    """
    查询拥有最多已发布 (Done) 文章的用户。
    如果有多人并列第一，返回包含这些用户的列表；如果只有一人，也返回列表；
    如果没有符合条件的数据，返回空列表。
    """
    # 1. 创建 CTE（公用表表达式），统计每个 person_id 对应的 Done 状态文章数量
    post_counts = (
        select(Post.person_id, func.count(Post.id).label("done_count"))
        .where(Post.status == PostStatus.Done)
        .group_by(Post.person_id)
        .cte("post_counts")
    )

    # 2. 创建子查询，获取最大的文章数量
    max_count_subq = select(func.max(post_counts.c.done_count)).scalar_subquery()

    # 3. 主查询：关联 Person 表，筛选出文章数量等于最大值的用户
    stmt = (
        select(Person)
        .join(post_counts, Person.id == post_counts.c.person_id)
        .where(post_counts.c.done_count == max_count_subq)
    )
    return list(session.scalars(stmt).all())


def get_recent_undone_posts(session: Session, _limit: int = 20) -> list[Post]:
    """
    查询状态不是已发布 (Done) 的文章，按创建时间倒序排列，并限制返回数量。
    """
    stmt = select(Post).where(Post.status != PostStatus.Done).order_by(Post.created_at.desc()).limit(_limit)

    return list(session.scalars(stmt).all())


def get_persons_without_posts(session: Session) -> list[Person]:
    """
    查询还没有任何文章 (Post) 的用户。
    对应 SQL: SELECT * FROM person WHERE NOT EXISTS (SELECT 1 FROM post WHERE post.person_id = person.id);
    """
    # 使用 ORM 提供的 .any() 方法取反，这是最优雅且高效的写法
    stmt = select(Person).where(~Person.posts.any())

    return list(session.scalars(stmt).all())


def get_all_unique_tags(session: Session) -> list[str]:
    """
    获取所有文章中出现过的不重复的标签 (tags)。
    对应 SQL: SELECT DISTINCT unnest(tags) FROM post;
    """
    # 使用 func.unnest 将数组展开为多行，然后使用 distinct 去重
    stmt = select(func.unnest(Post.tags)).distinct()

    return list(session.scalars(stmt).all())


def add_unique_tag_to_post(session: Session, post_id: int, tag: str) -> Optional[Post]:
    """
    给指定的文章 (Post) 增加一个标签 (tag)。
    如果该 tag 已经存在于 tags 列表中，则不做任何操作。
    """
    post = session.get(Post, post_id)

    if post and tag not in post.tags:
        post.tags.append(tag)
        session.commit()

    return post


def get_person_age(session: Session, person_id: int) -> Optional[int]:
    """
    获取指定用户的年龄。
    通过获取用户的 birthday 并在 Python 层进行计算。如果用户不存在或没有设置生日，返回 None。
    """
    person = session.get(Person, person_id)

    if person is None or person.birthday is None:
        return None

    birthday = person.birthday
    age = pendulum.datetime(birthday.year, birthday.month, birthday.day).age
    return age


if __name__ == "__main__":
    """
    output something

    """
    # ret = get_all_articles(Session(engine))
    # print(ret)
    # create_tables(engine)
    ret = get_person_age(Session(engine), 19)
    print(ret)
