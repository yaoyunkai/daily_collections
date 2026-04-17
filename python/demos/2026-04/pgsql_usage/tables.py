import reprlib
from datetime import date, datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    ARRAY,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    TypeDecorator,
    func,
    text,
)
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

_repr_obj = reprlib.Repr()
_repr_obj.maxstring = 20


class PostStatus(Enum):
    Draft = "S"  # 草稿
    ToReview = "T"  # 待审核
    Done = "D"  # 已发布


class GenderType(Enum):
    Unknown = "N"
    Man = "M"
    Woman = "W"


class StrEnumType(TypeDecorator):
    impl = String(1)
    cache_ok = True

    def __init__(self, enum_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enum_type = enum_type

    def process_bind_param(self, value, dialect):
        """
        force raise error while value is not self._enum_type

        """
        if value is None:
            return None
        if type(value) is not self._enum_type:
            raise TypeError('')

        return value.value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self._enum_type(value)


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "person"
    __table_args__ = (CheckConstraint("gender = ANY (ARRAY['N', 'M', 'W'])", name="person_gender_check"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    gender: Mapped[str] = mapped_column(String(1), server_default=text("'N'"))
    birthday: Mapped[Optional[date]] = mapped_column(Date)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now()"))

    post: Mapped[list["Post"]] = relationship("Post", back_populates="person")

    def __repr__(self) -> str:
        return f"<Person(id={self.id}, name={self.name!r}, gender={self.gender!r})>"


class Post(Base):
    __tablename__ = "post"
    __table_args__ = (CheckConstraint("status = ANY (ARRAY['S', 'D', 'P'])", name="post_status_check"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    person_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Person.id))

    tags: Mapped[list[str]] = mapped_column(
        MutableList.as_mutable(ARRAY(String(length=20))),
        default=list,
        server_default="'{}'",
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(1), nullable=False, server_default=text("'D'"))
    created_at: Mapped[datetime] = mapped_column(DateTime(True), server_default=func.now())
    content: Mapped[Optional[str]] = mapped_column(Text)

    person: Mapped[Optional["Person"]] = relationship("Person", back_populates="post")

    def __repr__(self) -> str:
        return (
            f"<Post(id={self.id}, title={_repr_obj.repr(self.title)}, "
            f"content={_repr_obj.repr(self.content)}, status={self.status!r})>"
        )


if __name__ == "__main__":
    print(GenderType.Man)

    ret = GenderType("M")
    print(ret)

    print(type(ret))
    print(isinstance(ret, GenderType))
