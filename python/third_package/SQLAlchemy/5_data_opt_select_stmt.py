"""
Select Usage


"""

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import insert
from sqlalchemy import literal_column
from sqlalchemy import select
from sqlalchemy import text

engine = sqlalchemy.create_engine("sqlite+pysqlite:///:memory:", echo=True)

metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30), nullable=False),
    Column("fullname", String),
)

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

with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()

"""
select start


"""
stmt = select(user_table).where(user_table.c.name == "spongebob")
# print(stmt)

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)

"""
stmt = select(User).where(User.name == "spongebob")
with Session(engine) as session:
    for row in session.execute(stmt):
        print(row)
"""

print(select(user_table))

print(select(user_table.c.name, user_table.c.fullname))

print(select(user_table.c["name", "fullname"]))

stmt = select(("Username: " + user_table.c.name).label("username"), ).order_by(user_table.c.name)

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(f"{row.username}")

stmt = select(text("'some phrase'"), user_table.c.name).order_by(user_table.c.name)

with engine.connect() as conn:
    print(conn.execute(stmt).all())

stmt = select(literal_column("'some phrase'").label("p"), user_table.c.name).order_by(
    user_table.c.name
)
with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(f"{row.p}, {row.name}")

"""
Where clause


"""
print(user_table.c.name == "squidward")
print(address_table.c.user_id > 10)

print(select(user_table).where(user_table.c.name == "squidward"))

"""
这两种写法对where的连接都是 AND

"""
print(
    select(address_table.c.email_address)
    .where(user_table.c.name == "squidward")
    .where(address_table.c.user_id == user_table.c.id)
)
print(
    select(address_table.c.email_address).where(user_table.c.name == "squidward",
                                                address_table.c.user_id == user_table.c.id, )
)

"""
JOIN

"""
print(select(user_table.c.name, address_table.c.email_address))

print(
    select(user_table.c.name, address_table.c.email_address).join_from(
        user_table, address_table
    )
)

print(select(user_table.c.name, address_table.c.email_address).join(address_table))

print(select(address_table.c.email_address).select_from(user_table).join(address_table))
