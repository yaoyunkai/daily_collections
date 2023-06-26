"""

Database Metadata
Metadata, Column, Table

Type Hints: https://peps.python.org/pep-0484/
            https://peps.python.org/pep-0483/

使用 table.c 来访问 columns

metadata.drop_all()

----------------------------------------------------


Created at 2023/6/26
"""

import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table

engine = sqlalchemy.create_engine("sqlite+pysqlite:///:memory:", echo=True)

metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

# print(user_table.c.name)
# print(user_table.c.keys())
# print(user_table.primary_key)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)

# metadata_obj.create_all(engine)
