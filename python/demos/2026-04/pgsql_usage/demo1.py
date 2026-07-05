"""
demo1.py



created at 2026-07-03
"""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_engine(
    "postgresql+psycopg://test1:test1@localhost:5432/demo1",
    connect_args={"options": "-c timezone=UTC", "connect_timeout": 3},
    echo=True,
)


class Base(DeclarativeBase):
    pass


class PayRecord(Base):
    __tablename__ = "demo_pay_record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[str] = mapped_column(String(32), nullable=False)
    amount: Mapped[int] = mapped_column(Integer)
    pay_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


if __name__ == "__main__":
    pass
