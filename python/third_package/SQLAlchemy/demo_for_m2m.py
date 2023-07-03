"""


Created at 2023/7/3
"""

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# 中间表定义
article_tag_association = Table(
    'article_tag_association',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)

    # 定义与标签的多对多关系
    tags = relationship('Tag', secondary=article_tag_association, back_populates='articles')


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # 定义与文章的多对多关系
    articles = relationship('Article', secondary=article_tag_association, back_populates='tags')
