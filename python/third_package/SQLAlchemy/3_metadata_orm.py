"""
DeclarativeBase

DeclarativeBase.metadata
DeclarativeBase.registry

DeclarativeBase.__table__ --> for access the Table object

mapped_column / Mapped

-------------------------------------
table reflection

some_table = Table("some_table", metadata_obj, autoload_with=engine)



Created at 2023/6/26
"""
from typing import List, Optional

import sqlalchemy
from sqlalchemy import ForeignKey, String, insert
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = sqlalchemy.create_engine("sqlite+pysqlite:///:memory:", echo=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    自动生成 __init__

    """
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


# print(User.__table__)
# print(type(User.__table__))

Base.metadata.create_all(engine)
