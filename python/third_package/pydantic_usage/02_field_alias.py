"""


Created at 2023/8/14
"""
import typing

import sqlalchemy as sa
from pydantic import BaseModel
from pydantic import Field
from sqlalchemy.orm import DeclarativeBase


class MyModel(BaseModel):
    metadata: typing.Dict[str, str] = Field(alias='metadata_')

    class Config:
        orm_mode = True


class Base(DeclarativeBase):
    pass


class SQLModel(Base):
    __tablename__ = 'my_table'
    id = sa.Column('id', sa.Integer, primary_key=True)
    # 'metadata' is reserved by SQLAlchemy, hence the '_'
    metadata_ = sa.Column('metadata', sa.JSON)


sql_model = SQLModel(metadata_={'key': 'val'}, id=1)

pydantic_model = MyModel.from_orm(sql_model)

print(pydantic_model.dict())

print(pydantic_model.dict(by_alias=True))
