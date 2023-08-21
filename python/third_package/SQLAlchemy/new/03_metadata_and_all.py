"""
Created at 2023/8/18

DeclarativeBase.registry

Insert class 的参数可以被execute传入的参数覆盖


"""

from typing import List
from typing import Optional

from sqlalchemy import Column, Integer, String, Table, select
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData
from sqlalchemy import and_, or_
from sqlalchemy import bindparam
from sqlalchemy import create_engine
from sqlalchemy import desc, func
from sqlalchemy import insert
from sqlalchemy import literal_column
from sqlalchemy.dialects import oracle, postgresql
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import aliased
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

metadata_obj = MetaData()

# engine = create_engine(
#     url="postgresql+psycopg2://user1:password@localhost/simple_230808", echo=True
# )

engine = create_engine(
    url="mysql+mysqldb://root:password@localhost/sql_adv", echo=True
)

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
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


def xprint_columns():
    print(user_table.c.name)
    print(user_table.c.keys())

    print(user_table.primary_key)

    # print(address_table.foreign_keys)
    # 
    # for key in address_table.foreign_keys:
    #     print(key)


def check_metadata():
    print(metadata_obj == Base.metadata)


def create_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def base_attributes():
    print(type(User.__table__))

    print(User(id=1, name='Tom', fullname='Tom Peter'))


def insert_sql_metadata():
    stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")
    print(stmt)
    print(stmt.__class__.__mro__)

    complied = stmt.compile(engine)
    print(complied)
    print(complied.params)

    # with engine.connect() as conn:
    #     result = conn.execute(stmt, [{'name': 'tom', 'fullname': 'bob tom'}])
    #     conn.commit()
    #
    #     # 返回tuple的原因: 有联合主键
    #     print(result.inserted_primary_key)

    with engine.connect() as conn:
        # insert 没有 values的时候会自动根据传入的参数判断
        result = conn.execute(
            insert(user_table),
            [
                {"name": "sandy", "fullname": "Sandy Cheeks"},
                {"name": "patrick", "fullname": "Patrick Star"},
            ],
        )
        # conn.commit()

        # print(result.rowcount)

    print(insert(user_table).values().compile(engine))

    # insert returning
    insert_stmt = insert(address_table).returning(
        address_table.c.id, address_table.c.email_address
    )
    print(insert_stmt)

    comp = insert_stmt.compile(engine)
    print(comp)

    select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
    insert_stmt = insert(address_table).from_select(
        ["user_id", "email_address"], select_stmt
    )
    print(insert_stmt)
    comp = insert_stmt.compile(engine)
    print(comp)


def insert_sql_adv():
    """
    insert into address (user_id, email_address)
    values ((select user_account.id from user_account where
    user_account.name = 'spongebob'), 'spongebob@sqlalchemy.org');

    """
    scalar_subq = (select(user_table.c.id).where(user_table.c.name == bindparam("username")).scalar_subquery())
    insert_sql = insert(address_table).values(user_id=scalar_subq)

    with engine.connect() as conn:
        conn.execute(
            insert_sql,
            [
                {"username": "spongebob", "email_address": "spongebob@sqlalchemy.org"},
                {"username": "sandy", "email_address": "sandy@sqlalchemy.org"},
                {"username": "sandy", "email_address": "sandy@squirrelpower.org"},
            ],
        )
        conn.commit()


def select_sql_metadata():
    stmt = select(user_table).where(user_table.c.name == "spongebob")
    print(stmt)

    with engine.connect() as conn:
        for row in conn.execute(stmt, ):
            print(row)

    stmt = select(User).where(User.name == "spongebob")
    with Session(engine) as session:
        for row in session.execute(stmt):
            print(row)

    print(select(user_table))
    print(select(user_table.c.name, user_table.c.fullname))
    print(select(user_table.c["name", "fullname"]))

    print(select(User))

    # 即便是first也会返回一个序列
    row = session.execute(select(User)).first()
    print(type(row))
    print(row)

    print(row[0])

    user = session.scalars(select(User)).first()
    print(user)
    print(type(user))

    # 选择不同的行
    print(select(User.name, User.fullname))

    row = session.execute(select(User.name, User.fullname))
    for item in row:
        print(item)

    result = session.execute(
        select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
    ).all()
    print(result)

    print('----------------------------------------\n')

    # 别名
    stmt = select(("Username: " + user_table.c.name).label("username"), ).order_by(user_table.c.name)
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(f"{row.username}")

    stmt = select(literal_column("'some phrase'").label("p"), user_table.c.name).order_by(
        user_table.c.name
    )
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            print(f"{row.p}, {row.name}")


def where_in_select_sql():
    print(user_table.c.name == "squidward")
    print(address_table.c.user_id > 10)

    print(select(user_table).where(user_table.c.name == "squidward"))

    print(
        select(address_table.c.email_address)
        .where(user_table.c.name == "squidward")
        .where(address_table.c.user_id == user_table.c.id)
    )

    # print(
    #     select(address_table.c.email_address).where(
    #         user_table.c.name == "squidward", address_table.c.user_id == user_table.c.id,
    #     )
    # )

    print(
        select(Address.email_address).where(
            and_(
                or_(User.name == "squidward", User.name == "sandy"),
                Address.user_id == User.id,
            )
        )
    )

    print(select(User).filter_by(name="spongebob", fullname="Spongebob Squarepants"))


def from_in_select_sql():
    """
    TODO join_from join 的区别

    """
    print(select(user_table.c.name, address_table.c.email_address))

    # 自动查找外键关系
    print(
        select(user_table.c.name, address_table.c.email_address).join_from(
            user_table, address_table
        )
    )

    print(select(user_table.c.name, address_table.c.email_address).join(address_table))
    print(select(address_table.c.email_address).select_from(user_table).join(address_table))

    print(select(func.count("*")).select_from(user_table))

    # 指明on的条件
    print(
        select(address_table.c.email_address)
        .select_from(user_table)
        .join(address_table, user_table.c.id == address_table.c.user_id)
    )

    # left outer join, full join
    # 等于left join和right join的并集
    print(select(user_table).join(address_table, isouter=True))
    print(select(user_table).join(address_table, full=True))


def order_by_in_select():
    print(select(user_table).order_by(user_table.c.name.asc()))
    print(select(User).order_by(User.fullname.desc()))

    stmt = func.count(user_table.c.id)
    print(stmt)

    with engine.connect() as conn:
        result = conn.execute(
            select(User.name, func.count(Address.id).label("count"))
            .join(Address)
            .group_by(User.name)
            .having(func.count(Address.id) > 1)
        )
        print(result.all())

    # group_by order_by 既可以传递字符串，也可以传递column实例
    stmt = (
        select(Address.user_id, func.count(Address.id).label("num_addresses"))
        .group_by(Address.user_id)
        .order_by("user_id", desc("num_addresses"))
    )
    print(stmt)

    # 使用别名来引用同一个表
    user_alias_1 = user_table.alias()
    print(f'type is : {type(user_alias_1)}')

    user_alias_2 = user_table.alias()
    print(
        select(user_alias_1.c.name, user_alias_2.c.name).join_from(
            user_alias_1, user_alias_2, user_alias_1.c.id > user_alias_2.c.id
        )
    )

    # ORM 使用方法 aliased
    address_alias_1 = aliased(Address)
    address_alias_2 = aliased(Address)
    print(
        select(User)
        .join_from(User, address_alias_1)
        .where(address_alias_1.email_address == "patrick@aol.com")
        .join_from(User, address_alias_2)
        .where(address_alias_2.email_address == "patrick@gmail.com")
    )


def scalar_subquery_sql():
    subq = (
        select(func.count(address_table.c.id))
        .where(user_table.c.id == address_table.c.user_id)
        .scalar_subquery()
    )
    print(subq)

    print(subq == 5)

    stmt = select(user_table.c.name, subq.label("address_count"))
    print(stmt)

    subq = (
        select(func.count(address_table.c.id))
        .where(user_table.c.id == address_table.c.user_id)
        .group_by(address_table.c.user_id)
        .having(func.count(address_table.c.id) > 1)
    ).exists()
    with engine.connect() as conn:
        result = conn.execute(select(user_table.c.name).where(subq))
        print(result.all())


def sql_function():
    print(select(func.count()).select_from(user_table))

    print(select(func.lower("A String With Much UPPERCASE")))

    with engine.connect() as conn:
        result = conn.execute(select(func.lower("A String With Much UPPERCASE")))
        print(result.all())

    stmt = select(func.now())
    with engine.connect() as conn:
        result = conn.execute(stmt)
        print(result.all())

    # func 是一个class, 由于sql的方法很多 所以func支持任何传入的属性
    print(select(func.some_crazy_function(user_table.c.name, 17)))

    print(select(func.now()).compile(dialect=postgresql.dialect()))
    print(select(func.now()).compile(dialect=oracle.dialect()))

    #  "SQL 返回类型"，指的是函数在数据库侧 SQL 表达式中返回的 SQL 值类型，而不是 Python 函数的 "返回类型"。
    print(func.now().type)


if __name__ == '__main__':
    # print_columns()
    # check_metadata()
    # create_db()
    # base_attributes()

    # insert_sql_metadata()
    # insert_sql_adv()

    # select_sql_metadata()
    # from_in_select_sql()
    # scalar_subquery_sql()
    sql_function()
