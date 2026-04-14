"""
create_dummy_data.py


created at 2026-04-14
"""

import random

import factory
from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy.orm import Session
from tables import DummyArticle, GenderType, Person, Post, PostStatus

MAN_WOMEN = [GenderType.Man, GenderType.Woman]
LOCALES = "zh_CN"


# ==========================================
# 1. 定义 Factory
# ==========================================
class PersonFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Person
        # 使用 flush 提升批量插入性能，最后由外部统一 commit
        sqlalchemy_session_persistence = "flush"

    name = factory.Faker("name", locale=LOCALES)
    gender = factory.Faker("random_element", elements=[g.value for g in MAN_WOMEN])
    birthday = factory.Faker("date_of_birth", minimum_age=18, maximum_age=80)


class PostFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Post
        sqlalchemy_session_persistence = "flush"

    title = factory.Faker("sentence", locale=LOCALES, nb_words=6)
    content = factory.Faker("text", locale=LOCALES, max_nb_chars=200)
    status = factory.Faker("random_element", elements=[s.value for s in PostStatus])
    # person 关系字段将会在生成时动态传入


class DummyArticleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = DummyArticle
        sqlalchemy_session_persistence = "flush"

    class Params:
        is_empty_content = factory.Faker("boolean", chance_of_getting_true=20)

    title = factory.Faker("sentence", nb_words=4, locale="zh_CN")
    tags = factory.Faker("words", nb=3, locale="zh_CN")
    content = factory.Maybe(
        "is_empty_content",
        yes_declaration=None,
        no_declaration=factory.Faker(
            "text",
            max_nb_chars=300,
            locale="zh_CN",
        ),
    )


# ==========================================
# 2. 实现生成逻辑
# ==========================================
def generate_dummy_data(session: Session):
    # 动态绑定当前数据库 Session 到 Factory
    PersonFactory._meta.sqlalchemy_session = session
    PostFactory._meta.sqlalchemy_session = session

    # 1. 批量创建 20 个 Person
    persons = PersonFactory.create_batch(20)

    # 2. 核心逻辑：保证每个 Person 至少有 1 个 Post (消耗 20 个 Post 名额)
    for person in persons:
        PostFactory(person=person)

    # 3. 核心逻辑：剩下的 80 个 Post 随机分配给这 20 个 Person
    for _ in range(80):
        # random.choice 随机抽取一个 person 实例赋值给外键关系
        PostFactory(person=random.choice(persons))

    # 统一提交事务到数据库
    session.commit()


def generate_dummy_articles(session: Session, count: int = 50):
    """
    批量生成纯中文的 DummyArticle 数据
    """
    DummyArticleFactory._meta.sqlalchemy_session = session
    articles = DummyArticleFactory.create_batch(count)
    session.commit()
    print(f"✅ 成功生成并插入了 {count} 条纯中文 DummyArticle 数据！")
    return articles


if __name__ == "__main__":
    from postgresql_usage import engine

    # generate_dummy_data(Session(engine))
    generate_dummy_articles(Session(engine))
