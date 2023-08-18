"""
Created at 2023/8/18

DeclarativeBase.registry


"""

from typing import List
from typing import Optional

from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

metadata_obj = MetaData()

engine = create_engine(
    url="postgresql+psycopg2://user1:password@localhost/simple_230808", echo=True
)

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)


class Base(DeclarativeBase):
    pass


class User(Base):
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


def print_columns():
    print(user_table.c.name)
    print(user_table.c.keys())

    print(user_table.primary_key)

    # print(address_table.foreign_keys)
    # 
    # for key in address_table.foreign_keys:
    #     print(key)


def check_metadata():
    print(metadata_obj == Base.metadata)


if __name__ == '__main__':
    # print_columns()
    # check_metadata()
    pass
