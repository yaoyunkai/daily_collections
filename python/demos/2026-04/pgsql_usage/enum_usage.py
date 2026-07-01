"""
enum_usage.py

https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum

https://python-statemachine.readthedocs.io/en/latest/


created at 2026-07-01
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Integer, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.types import Enum as SQLEnum
from statemachine import State, StateMachine

engine = create_engine(
    "postgresql+psycopg://test1:test1@localhost:5432/demo1",
    connect_args={"options": "-c timezone=UTC", "connect_timeout": 10},
    echo=True,
)


class Base(DeclarativeBase):
    pass


class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderStateMachine(StateMachine):
    pending = State("Pending", initial=True, value=OrderStatus.PENDING)
    paid = State("Paid", value=OrderStatus.PAID)
    shipped = State("Shipped", value=OrderStatus.SHIPPED)
    delivered = State("Delivered", final=True, value=OrderStatus.DELIVERED)
    cancelled = State("Cancelled", final=True, value=OrderStatus.CANCELLED)

    # events
    user_paid = pending.to(paid)
    user_unpaid = pending.to(cancelled)
    shop_ship = paid.to(shipped)
    user_signed = shipped.to(delivered)


class Order(Base):
    __tablename__ = "demo_order"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    order_no: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    order_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    order_status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(
            OrderStatus,
            native_enum=False,
            values_callable=lambda obj: [item.value for item in obj],
            length=32,
        ),
        nullable=False,
        default=OrderStatus.PENDING,
        server_default=OrderStatus.PENDING,  # 数据库层默认值设为字符串 "pending"
    )

    @property
    def machine(self) -> "OrderStateMachine":
        return OrderStateMachine(self, state_field="order_status")


def check_model_ddl():
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.schema import CreateTable

    create_ddl = CreateTable(Order.__table__)
    print(create_ddl.compile(dialect=postgresql.dialect()))


def play_with_sm():
    obj1 = OrderStateMachine()
    print(f"current state: {obj1.configuration}")
    obj1.user_paid()
    print(f"current state: {obj1.configuration}")

    obj2 = OrderStateMachine(start_value=OrderStatus.PAID)
    print(f"obj2 current state: {obj2.configuration}")


def play_with_demo_order():
    stmt = select(Order).order_by(Order.order_created_at.desc())

    session = Session(engine)
    # with session:
    # order1 = Order(order_no="001")
    # order2 = Order(order_no="002", order_status=OrderStatus.SHIPPED)
    # session.add(order1)
    # session.add(order2)
    # session.commit()

    # with session:
    #     order3 = Order(order_no="005", order_status=OrderStatus.DELIVERED)
    #     session.add(order3)
    #     session.commit()

    for order in session.scalars(stmt):
        # print(order)
        # print(order.order_status)
        print(order.machine.configuration)


if __name__ == "__main__":
    play_with_demo_order()
    # check_model_ddl()
    # play_with_sm()
