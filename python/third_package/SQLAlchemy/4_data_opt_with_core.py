"""
Insert Usage

Created at 2023/6/26
"""

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import insert
from sqlalchemy import select

engine = sqlalchemy.create_engine("sqlite+pysqlite:///:memory:", echo=True)

metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30), nullable=False),
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

metadata_obj.create_all(engine)

# Insert 实例
stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")
print(stmt)

compiled = stmt.compile()
print(compiled)
print(compiled.params)

with engine.connect() as conn:
    result = conn.execute(stmt)
    print(result.inserted_primary_key)
    conn.commit()
    print(result.inserted_primary_key)

# automatically
print(insert(user_table))

with engine.connect() as conn:
    # TODO pretty good
    result = conn.execute(
        insert(user_table),
        # 不支持不同字典的参数
        [
            {"name": "patrick", "fullname": "Patrick Star"},
            {"name": "sandy", "fullname": "Sandy Cheeks"},

        ],
    )
    conn.commit()

# all default values
print(insert(user_table).values().compile(engine))

# ===================================================================
insert_stmt = insert(address_table).returning(
    address_table.c.id, address_table.c.email_address
)
print(insert_stmt)

# ===================================================================
select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
insert_stmt = insert(address_table).from_select(
    ["user_id", "email_address"], select_stmt
)
print(insert_stmt.returning(address_table.c.id, address_table.c.email_address))

# ====================================================================
select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
insert_stmt = insert(address_table).from_select(
    ["user_id", "email_address"], select_stmt
)
print(insert_stmt)
