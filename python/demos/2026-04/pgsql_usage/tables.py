import reprlib
from datetime import date, datetime
from enum import StrEnum
from typing import Optional

from sqlalchemy import (
    ARRAY,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import Enum as SQLEnum

_repr_obj = reprlib.Repr()
_repr_obj.maxstring = 20


class PostStatus(StrEnum):
    Draft = "draft"  # 草稿
    ToReview = "to_review"  # 待审核
    Done = "done"  # 已发布


class GenderType(StrEnum):
    Unknown = "unknown"
    Man = "man"
    Woman = "woman"


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    gender: Mapped[GenderType] = mapped_column(
        SQLEnum(
            GenderType,
            native_enum=False,
            length=20,
            values_callable=lambda obj: [e.value for e in obj],
        ),
        default=GenderType.Unknown,
    )
    birthday: Mapped[Optional[date]] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="person")

    def __repr__(self) -> str:
        return f"<Person(id={self.id}, name={self.name!r}, gender={self.gender!r})>"


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey(Person.id), nullable=False)

    tags: Mapped[list[str]] = mapped_column(
        MutableList.as_mutable(ARRAY(String(length=20))),
        default=list,
        server_default="{}",
    )
    title: Mapped[str] = mapped_column(String(100))
    status: Mapped[PostStatus] = mapped_column(
        SQLEnum(
            PostStatus,
            native_enum=False,
            length=20,
            values_callable=lambda obj: [e.value for e in obj],
        ),
        default=PostStatus.Draft,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    content: Mapped[Optional[str]] = mapped_column(Text)

    person: Mapped["Person"] = relationship("Person", back_populates="posts")

    def __repr__(self) -> str:
        return (
            f"<Post(id={self.id}, title={_repr_obj.repr(self.title)}, "
            f"content={_repr_obj.repr(self.content)}, status={self.status!r})>"
        )
