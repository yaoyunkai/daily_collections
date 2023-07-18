"""

https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html

打卡记录
请假记录


Created at 2023/7/14
"""
import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from ..database import Base

TYPE_IN = 'in'
TYPE_OUT = 'out'


def is_valid_record_type(record_type: str) -> bool:
    if record_type == TYPE_OUT or record_type == TYPE_IN:
        return True
    return False


class AttendanceRecord(Base):
    __tablename__ = 'attendance_record'

    id: Mapped[int] = mapped_column(primary_key=True)
    staff_id: Mapped[str] = mapped_column(String(length=12))
    staff_name: Mapped[str] = mapped_column(String(length=64))

    record_time: Mapped[datetime.datetime]
    record_machine: Mapped[str] = mapped_column(String(length=64))
    record_type: Mapped[str] = mapped_column(String(length=3))
