import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    func,
    text,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class PassFail(Enum):
    Start = "start"
    Pass = "pass"
    Fail = "fail"


class Base(DeclarativeBase):
    pass


class TestRecord(Base):
    __tablename__ = "test_record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    record_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

    sernum: Mapped[str] = mapped_column(String(50))
    uuttype: Mapped[str] = mapped_column(String(50))
    test_area: Mapped[str] = mapped_column(String(20))

    passfail: Mapped[PassFail] = mapped_column(
        SQLEnum(PassFail, native_enum=False, length=10, values_callable=lambda obj: [e.value for e in obj])
    )

    runtime: Mapped[int] = mapped_column(Integer)
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

    first_pass_flag: Mapped[Optional[bool]] = mapped_column(Boolean)
    synced_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
