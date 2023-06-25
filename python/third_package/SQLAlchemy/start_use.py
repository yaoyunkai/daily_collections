"""
建立连接


"""

import sqlalchemy

print(sqlalchemy.__version__)

"""
sqlite: 哪种数据库 dialect
pysqlite: DBAPI

lazy connection

"""
engine = sqlalchemy.create_engine("sqlite+pysqlite:///:memory:", echo=True)
