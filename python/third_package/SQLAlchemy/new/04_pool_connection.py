"""

pool_recycle
pool_timeout

Mapped -> mapped_column


mapped_column nullable: 控制数据库是否为null
Mapped Optional:        控制python是否可以为null

Created at 2023/8/22
"""
import datetime
import decimal
import uuid
from typing import Any, Dict, Type
from typing import Optional

from sqlalchemy import Column, Integer, String, Table, create_engine, types
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.type_api import TypeEngine

# engine = create_engine(
#     url="mysql+mysqldb://root:password@localhost/sql_adv", echo=True,
#     # pool_size=20, max_overflow=0
# )

engine = create_engine(
    url="sqlite:///foo.db", echo=True,
    # pool_size=20, max_overflow=0
)

type_map: Dict[Type[Any], TypeEngine[Any]] = {
    bool: types.Boolean(),
    bytes: types.LargeBinary(),
    datetime.date: types.Date(),
    datetime.datetime: types.DateTime(),
    datetime.time: types.Time(),
    datetime.timedelta: types.Interval(),
    decimal.Decimal: types.Numeric(),
    float: types.Float(),
    int: types.Integer(),
    str: types.String(),
    uuid.UUID: types.Uuid(),
}


class Base(DeclarativeBase):
    pass


class SomeClass(Base):
    __tablename__ = "some_table"

    # primary_key=True, therefore will be NOT NULL
    id: Mapped[int] = mapped_column(primary_key=True)

    # not Optional[], therefore will be NOT NULL
    data1: Mapped[str]

    # Optional[], therefore will be NULL
    additional_info: Mapped[Optional[str]]

    # will be String() NOT NULL, but can be None in Python
    data2: Mapped[Optional[str]] = mapped_column(nullable=False)

    # will be String() NULL, but type checker will not expect
    # the attribute to be None
    data3: Mapped[str] = mapped_column(nullable=True)


user_table = Table(
    "user",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("fullname", String),
    Column("nickname", String),
)


# construct the User class using this table.
class User(Base):
    __table__ = user_table


if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    pass
