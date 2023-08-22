"""


Created at 2023/8/22
"""
from typing import List, Optional

from sqlalchemy import ForeignKey, String, bindparam, select
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

engine = create_engine(
    url="mysql+mysqldb://root:password@localhost/sql_adv", echo=True,
    # pool_size=20, max_overflow=0
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


def select_stmt():
    session = Session(engine)

    stmt = select(User).where(User.id == bindparam('id'))

    result = session.execute(stmt, {'id': 2})
    print(result, type(result))
    print(type(result.all()))

    ret = session.scalars(select(User).order_by(User.id))
    print(ret, type(ret))
    print(type(result.all()))

    stmt = select(User, Address).join(User.addresses).order_by(User.id, Address.id)
    for row in session.execute(stmt):
        print(f"{row.User.name} {row.Address.email_address}")

    result = session.execute(
        select(User.name, Address.email_address)
        .join(User.addresses)
        .order_by(User.id, Address.id)
    )
    for row in result:
        print(f"{row.name}  {row.email_address}")

    textual_sql = text("SELECT `id`, `name`, `fullname` FROM `user_account` ORDER BY `id`")
    textual_sql = textual_sql.columns(User.id, User.name, User.fullname)
    orm_sql = select(User).from_statement(textual_sql)
    for user_obj in session.execute(orm_sql).scalars():
        print(user_obj)


if __name__ == '__main__':
    select_stmt()
