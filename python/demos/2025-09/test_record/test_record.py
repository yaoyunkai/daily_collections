import datetime
from enum import IntEnum, StrEnum
from typing import Optional

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Index,
    Integer,
    SmallInteger,
    String,
    func,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class FirstPassFlag(IntEnum):
    UNSET = -1
    TRUE = 1
    FALSE = 0


class PassFail(StrEnum):
    Start = "S"
    Pass = "P"
    Fail = "F"
    Sampling = "A"


class Base(DeclarativeBase):
    pass


class TestRecord(Base):
    __tablename__ = "test_record"
    __table_args__ = (
        CheckConstraint("passfail = ANY (ARRAY['A', 'S', 'P', 'F'])", name="test_record_passfail_check"),
        Index("idx_test_record_calc", "sernum", "test_area", "record_time"),
        Index("idx_test_record_unprocessed", "first_pass_flag", postgresql_where="(first_pass_flag = -1)"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    record_time: Mapped[datetime.datetime] = mapped_column(DateTime(True))

    sernum: Mapped[str] = mapped_column(String(50))
    uuttype: Mapped[str] = mapped_column(String(50))
    test_area: Mapped[str] = mapped_column(String(20))
    passfail: Mapped[PassFail] = mapped_column(String(1))
    runtime: Mapped[int] = mapped_column(Integer, server_default=text("0"))
    test_fail: Mapped[str] = mapped_column(String(50), server_default=text("''"))
    test_machine: Mapped[str] = mapped_column(String(20))
    test_container: Mapped[str] = mapped_column(String(50))
    test_mode: Mapped[str] = mapped_column(String(10), server_default=text("'PROD0'"))
    deviation: Mapped[str] = mapped_column(String(16), server_default=text("'D000000'"))

    testr1name: Mapped[Optional[str]] = mapped_column(String(50))
    testr1: Mapped[Optional[str]] = mapped_column(String(50))
    testr2name: Mapped[Optional[str]] = mapped_column(String(50))
    testr2: Mapped[Optional[str]] = mapped_column(String(50))
    testr3name: Mapped[Optional[str]] = mapped_column(String(50))
    testr3: Mapped[Optional[str]] = mapped_column(String(50))

    first_pass_flag: Mapped[FirstPassFlag] = mapped_column(
        SmallInteger,
        server_default=text("-1"),
        default=FirstPassFlag.UNSET,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=func.now())
