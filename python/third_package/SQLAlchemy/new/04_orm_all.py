"""
Created at 2023/8/21

select 时会自动打开一个事务

https://docs.sqlalchemy.org/en/20/orm/session_basics.html


"""
from typing import List, Optional

from sqlalchemy import ForeignKey, String, select
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

engine = create_engine(
    url="postgresql+psycopg2://user1:password@localhost/simple_230808", echo=True
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] = mapped_column(String(200))
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


def insert_sql_stmt():
    session = Session(engine)

    squidward = User(name="squidward", fullname="Squidward Tentacles")
    krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")

    print(squidward)
    print(krabs)

    session.add(squidward)
    session.add(krabs)

    # 待处理对象 IdentitySet 
    print(session.new)

    # 显式打开了一个事务，实际并未提交
    session.flush()

    # commit rollback close 的时候才会关闭事务
    print(squidward.id)
    print(krabs.id)

    # id map 会缓存DB的数据
    # 在事务中操作复杂的对象集
    person1 = session.get(User, squidward.id)
    print(person1)
    print(person1 == squidward)

    # 提交事务
    session.commit()

    # 之前的对象再次访问属性时，会重新开启新的事务
    print(squidward.id)


def update_sql_stmt():
    session = Session(engine)

    # scalar 会在返回多个行的时候报错
    sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
    print(sandy)

    sandy.fullname = "Sandy Squirrel"
    print(sandy in session.dirty)

    sandy_fullname = session.execute(select(User.fullname).where(User.id == sandy.id)).scalar_one()
    print(sandy_fullname)

    # 实际上数据还没提交到数据库
    print(sandy in session.dirty)


def delete_sql_stmt():
    session = Session(engine)
    patrick = session.get(User, 3)
    session.delete(patrick)

    # 当前的 ORM 行为是，patrick 会一直留在会话中，直到执行刷新操作
    session.execute(select(User).where(User.name == "patrick")).first()

    print(patrick in session)


def rollback_stmt():
    session = Session(engine)

    # scalar 会在返回多个行的时候报错
    sandy = session.execute(select(User).filter_by(name="sandy")).scalar_one()
    print(sandy)

    print(sandy.__dict__)

    sandy.fullname = "Sandy Squirrel"
    print(sandy in session.dirty)

    sandy_fullname = session.execute(select(User.fullname).where(User.id == sandy.id)).scalar_one()
    print(sandy_fullname)

    # 实际上数据还没提交到数据库
    print(sandy in session.dirty)

    session.rollback()

    print(sandy.__dict__)


def relationship_stmt():
    u1 = User(name="pkrabs", fullname="Pearl Krabs")
    print(u1.addresses)

    a1 = Address(email_address="pearl.krabs@gmail.com")
    u1.addresses.append(a1)

    print(u1.addresses)
    print(a1.user)

    a2 = Address(email_address="pearl@aol.com", user=u1)
    print(u1.addresses)

    print(a2.user == u1)

    print('================================')

    # work with session
    session = Session(engine)
    session.add(u1)
    print(a1 in session)

    session.commit()


def relationship_in_query():
    """
    ForeignKeyConstraint
    relationship()
    
    """
    
    print(select(Address.email_address).select_from(User).join(User.addresses))

    print(select(Address.email_address).join_from(User, Address))


if __name__ == '__main__':
    # insert_sql_stmt()
    # update_sql_stmt()
    # delete_sql_stmt()
    # rollback_stmt()
    # relationship_stmt()
    relationship_in_query()
