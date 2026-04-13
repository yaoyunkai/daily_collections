from datetime import date, datetime
from enum import StrEnum
from typing import Optional

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class PostStatus(StrEnum):
    Draft = "S"  # 草稿
    ToReview = "T"  # 待审核
    Done = "D"  # 已发布


class GenderType(StrEnum):
    Unknown = "N"
    Man = "M"
    Woman = "W"


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "person"
    __table_args__ = (PrimaryKeyConstraint("id", name="person_pkey"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default=GenderType.Unknown,
        server_default=GenderType.Unknown.value,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(True), nullable=False, server_default=text("now()"))
    birthday: Mapped[date | None] = mapped_column(Date, nullable=True)

    post: Mapped[list["Post"]] = relationship("Post", back_populates="person")


class Post(Base):
    __tablename__ = "post"
    __table_args__ = (
        ForeignKeyConstraint(["person_id"], ["person.id"], name="fk_post_person"),
        PrimaryKeyConstraint("id", name="post_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(60), nullable=False, comment="文章标题")
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default=PostStatus.Draft,
        server_default=PostStatus.Draft.value,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(True), nullable=False, server_default=text("now()"))
    person_id: Mapped[Optional[int]] = mapped_column(ForeignKey("person.id"))

    person: Mapped[Optional["Person"]] = relationship("Person", back_populates="post")
