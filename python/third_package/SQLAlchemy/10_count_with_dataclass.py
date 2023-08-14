"""


Created at 2023/8/14
"""
import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase

engine = sqlalchemy.create_engine("mysql+mysqldb://root:password@localhost/sakila", echo=True)

_sql = """
select actor_id, count(film_id) as cnt
from film_actor
group by actor_id
"""


class Base(DeclarativeBase):
    pass


class FilmCount(BaseModel):
    film_id: int
    cnt: int


with engine.connect() as conn:
    result = conn.execute(text(_sql))
    # print(result.all())

    arr = []
    for row in result.all():
        arr.append(FilmCount(film_id=row[0], cnt=row[1]))

    print(arr)
