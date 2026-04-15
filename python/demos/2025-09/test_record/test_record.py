import datetime
from enum import IntEnum, StrEnum
from typing import Optional

from sqlalchemy import (
    BigInteger,
    DateTime,
    Integer,
    SmallInteger,
    String,
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

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    record_time: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    sernum: Mapped[str] = mapped_column(String(50), nullable=False)
    uuttype: Mapped[str] = mapped_column(String(50), nullable=False)
    test_area: Mapped[str] = mapped_column(String(20), nullable=False)
    passfail: Mapped[PassFail] = mapped_column(String(1), nullable=False)
    runtime: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    test_fail: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("''"))
    test_machine: Mapped[str] = mapped_column(String(20), nullable=False)
    test_container: Mapped[str] = mapped_column(String(50), nullable=False)
    test_mode: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        server_default=text("'PROD0'::character varying"),
    )
    deviation: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        server_default=text("'D000000'::character varying"),
    )
    first_pass_flag: Mapped[FirstPassFlag] = mapped_column(
        SmallInteger,
        nullable=False,
        server_default=text("'-1'"),
        default=FirstPassFlag.UNSET,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text("now()"))
    testr1name: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("NULL::character varying"))
    testr1: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("NULL::character varying"))
    testr2name: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("NULL::character varying"))
    testr2: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("NULL::character varying"))
    testr3name: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("NULL::character varying"))
    testr3: Mapped[Optional[str]] = mapped_column(String(50), server_default=text("NULL::character varying"))
