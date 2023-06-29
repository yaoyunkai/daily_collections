"""

default type mapping
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

mapped_column 从 Mapped 取得俩个数据:
    datatype
    nullability

建表语句
CreateTable(SomeClass.__table__).compile(dialect=mssql.dialect())


==============================================================================
==============================================================================

str_30 = Annotated[str, 30]
str_50 = Annotated[str, 50]
num_12_4 = Annotated[Decimal, 12]
num_6_2 = Annotated[Decimal, 6]


### 将一个python 类型映射到做个SQL类型
class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            str_30: String(30),
            str_50: String(50),
            num_12_4: Numeric(12, 4),
            num_6_2: Numeric(6, 2),
        }
    )


==============================================================================
==============================================================================


from typing_extensions import Annotated

from sqlalchemy import func
from sqlalchemy import String
from sqlalchemy.orm import mapped_column


intpk = Annotated[int, mapped_column(primary_key=True)]
timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]
required_name = Annotated[str, mapped_column(String(30), nullable=False)]


Status = Literal["pending", "received", "completed"]


==============================================================================
==============================================================================

user_table = User.__table__
user_table = inspect(User).local_table


column_property: 一个用于定义基于现有列的计算属性的功能。
mapped_column.deferred: 延迟加载列




Created at 2023/6/29
"""

from datetime import datetime
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates


class Base(DeclarativeBase):
    # customize the type mapping
    # type_annotation_map = {
    #     int: BIGINT,
    #     datetime: TIMESTAMP(timezone=True),
    #     str: String().with_variant(NVARCHAR, "mssql"),
    # }
    pass


class User(Base):
    __tablename__ = "user"
    # __table_args__ = {"mysql_engine": "InnoDB"}

    #
    # __mapper_args__ = {"primary_key": [user_id, group_id]}

    # 自定义db的column名字
    # id: Mapped[int] = mapped_column("user_id", primary_key=True)
    # name: Mapped[str] = mapped_column("user_name")

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    fullname: Mapped[Optional[str]] = mapped_column(String(64))
    nickname: Mapped[Optional[str]] = mapped_column(String(64))
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "address"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    email_address: Mapped[str] = mapped_column(String(200))

    user: Mapped["User"] = relationship(back_populates="addresses")

    @validates("email_address")
    def validate_email(self, key, address):
        if "@" not in address:
            raise ValueError("failed simple email validation")
        return address
