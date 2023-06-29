"""

type annotation map.



Created at 2023/6/28
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


def start_use():
    u1 = User(name="pkrabs", fullname="Pearl Krabs")
    print(u1.addresses)

    a1 = Address(email_address="pearl.krabs@gmail.com")
    u1.addresses.append(a1)
    print(u1.addresses)

    print(a1.user)
    a2 = Address(email_address="pearl@aol.com", user=u1)
    print(u1.addresses)
    print(a2.user == u1)

    # =============================================================
    session.add(u1)
    print(u1 in session)
    print(a1 in session)
    print(a2 in session)

    session.commit()


def load_relationships():
    u1 = session.get(User, 1)
    print(u1)
    print(u1.addresses)


def use_join():
    print(select(Address.email_address).select_from(User).join(User.addresses))


if __name__ == '__main__':
    use_join()
