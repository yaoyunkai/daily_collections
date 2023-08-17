"""

ResultProxys

rowcount()
inserted_primary_key()

first()
fetchone()
fetchall()
scalar()     如果查询结果是包含一个列的单条记录，则返回单个值。

keys()       查看结果的列名

尽量使用可迭代对象 ResultProxy



Created at 2023/8/17
"""

from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer,
                        MetaData, Numeric, String, Table, create_engine)

metadata = MetaData()

cookies = Table('cookies', metadata,
                Column('cookie_id', Integer(), primary_key=True),
                Column('cookie_name', String(50), index=True),
                Column('cookie_recipe_url', String(255)),
                Column('cookie_sku', String(55)),
                Column('quantity', Integer()),
                Column('unit_cost', Numeric(12, 2))
                )

users = Table('users', metadata,
              Column('user_id', Integer(), primary_key=True),
              Column('username', String(15), nullable=False, unique=True),
              Column('email_address', String(255), nullable=False),
              Column('phone', String(20), nullable=False),
              Column('password', String(25), nullable=False),
              Column('created_on', DateTime(), default=datetime.now),
              Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
              )

orders = Table('orders', metadata,
               Column('order_id', Integer(), primary_key=True),
               Column('user_id', ForeignKey('users.user_id')),
               Column('shipped', Boolean(), default=False)
               )

line_items = Table('line_items', metadata,
                   Column('line_items_id', Integer(), primary_key=True),
                   Column('order_id', ForeignKey('orders.order_id')),
                   Column('cookie_id', ForeignKey('cookies.cookie_id')),
                   Column('quantity', Integer()),
                   Column('extended_cost', Numeric(12, 2))
                   )

engine = create_engine('sqlite:///:memory:')
metadata.create_all(engine)

# ==============================================
# Insert usage
#
#
from sqlalchemy import insert

# 插入语句
ins = cookies.insert().values(
    cookie_name="chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity="12",
    unit_cost="0.50"
)
print(ins)

# SQLCompiler
print(ins.compile().params)

connection = engine.connect()

result = connection.execute(ins)

print(result.inserted_primary_key)

ins_sql = insert(cookies).values(
    cookie_name="chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity="12",
    unit_cost="0.50"
)

print(ins_sql)
result = connection.execute(ins_sql)
print(result.inserted_primary_key)

ins_sql2 = cookies.insert()

result = connection.execute(
    ins_sql2,
    dict(cookie_name='dark chocolate chip',
         cookie_recipe_url='http://some.aweso.me/cookie/recipe_dark.html',
         cookie_sku='CC02',
         quantity='1',
         unit_cost='0.75')
)
print(result.inserted_primary_key)

# ============================================
# 使用 select 函数

from sqlalchemy import select

sel = select(cookies)

result = connection.execute(sel)
print(result.fetchall())

sel2 = cookies.select()

# print(sel2)
result = connection.execute(sel2)  # ReusltProxy
# print(result.fetchall())

first_row = result.fetchall()[0]

print(first_row[1])
print(first_row.cookie_name)
# print(first_row[cookies.c.cookie_name])
