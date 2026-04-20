"""
create_dummy_data.py


created at 2026-04-14
"""

import random

import factory
from factory.alchemy import SQLAlchemyModelFactory
from postgresql_usage import engine
from sqlalchemy.orm import sessionmaker
from tables import GenderType, Person, Post, PostStatus

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


class PersonFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Person
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("name")
    gender = factory.Faker("random_element", elements=list(GenderType))
    birthday = factory.Faker("date_of_birth")


class PostFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Post
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

    title = factory.Faker("sentence", nb_words=6)
    content = factory.Faker("text", max_nb_chars=200)
    tags = factory.Faker("words", nb=3)
    status = factory.Faker("random_element", elements=list(PostStatus))


def generate_dummy_data():
    print("开始生成 Person 数据...")
    persons = PersonFactory.create_batch(20)
    print(f"成功生成 {len(persons)} 个 Person。")

    print("开始生成 Post 数据并随机关联...")
    posts = []
    for _ in range(100):
        random_person = random.choice(persons)

        post = PostFactory.create(person=random_person)
        posts.append(post)

    print(f"成功生成 {len(posts)} 个 Post。")

    # print("\n--- 数据示例 ---")
    # for p in persons[:2]:
    #     print(p)
    #     print(f"  TA 的文章数量: {len(p.posts)}")
    #     for post in p.posts[:2]:  # 只打印前两篇
    #         print(f"    - {post}")


if __name__ == "__main__":
    generate_dummy_data()
