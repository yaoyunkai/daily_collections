"""
session = Session(engine)

# 标量数据
session.scalars(select(User)).first()



"""
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

url = 'mysql+mysqldb://root:password@localhost:3306/demo3?charset=utf8'
engine = create_engine(url, pool_recycle=3600, echo=True)
session = Session(engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    自动生成 __init__

    """
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] = mapped_column(String(50))
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(200))
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


def start_insert():
    squidward = User(name="squidward", fullname="Squidward Tentacles")
    krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")

    # print(squidward)
    # Base.metadata.create_all(engine)

    session.add(squidward)
    session.add(krabs)

    # 查看挂起的对象
    print(session.new)
    # just push transaction, not really insert data
    session.flush()
    print(squidward.id)
    print(krabs.id)


def get_object():
    user1 = session.get(User, 3)
    user2 = session.get(User, 3)
    print(user1)

    print(user1 == user2)

    user3 = User(id=3, name='1234', fullname='sadf')
    print(user1 == user3)


def update_object():
    user1 = session.get(User, 3)
    user1.fullname = 'Tissss JJJ'
    if user1 in session.dirty:
        print('user1 is dirty')

    user1_fullname = session.execute(select(User.fullname).where(User.id == 3)).scalar_one()
    print(user1_fullname)

    if user1 in session.dirty:
        print('user1 is dirty after update')


def delete_object():
    user1 = session.get(User, 3)
    session.delete(user1)


def rollback_object():
    user1 = session.get(User, 3)
    user1.fullname = 'Tissss JJJ'
    session.flush()
    print(user1.fullname)
    session.rollback()
    print(user1.__dict__)
    print(user1.fullname)
    print(user1.__dict__)


def close_session():
    """
    release all connection

    expunges all objects


    :return:
    """


if __name__ == '__main__':
    rollback_object()
