"""

Mapping styles
Declarative Mapping
Imperative Mapping

Mapper

User.__table__ get Table object

table = inspect(User).local_table
table = inspect(User).selectable

-----------------------------------------------------------
mapper = User.__mapper__

from sqlalchemy import inspect
mapper = inspect(User)

 __mapper_args__


Mapper 相当于 Django ORM 的 META
insp = inspect(User)
insp.columns
insp.columns.name
insp.all_orm_descriptors

insp.column_attrs

------------------------------------------------------------
Inspection for instance

insp = inspect(u1)
insp.mapper
insp.session
insp.persistent
insp.pending
insp.unloaded
insp.unmodified
insp.attrs.nickname.value



Created at 2023/6/29
"""
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship


# declarative base class
class Base(DeclarativeBase):
    pass


# an example mapping using the base
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    fullname: Mapped[str] = mapped_column(String(30))
    nickname: Mapped[Optional[str]]


# ==================================================================

mapper_registry = registry()

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("fullname", String(50)),
    Column("nickname", String(12)),
)


class User1:
    pass


class Address:
    pass


# mapper_registry.map_imperatively(User1, user_table)

address = Table(
    "address",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("email_address", String(50)),
)

mapper_registry.map_imperatively(
    User,
    user_table,
    properties={
        "addresses": relationship(Address, backref="user", order_by=address.c.id)
    },
)

mapper_registry.map_imperatively(Address, address)
