"""
Created at 2023/8/18

反射

table.columns
table.c
table.c.keys()


"""
from sqlalchemy import MetaData
from sqlalchemy import Table, create_engine

engine = create_engine(
    url="postgresql+psycopg2://user1:password@localhost/simple_230808", echo=False
)

metadata = MetaData()

some_table = Table('some_table', metadata, autoload_with=engine)

# op(some_table)
