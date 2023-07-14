"""

https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html


Created at 2023/7/14
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from ..database import Base


class AttendanceRecord(Base):
    __tablename__ = 'attendance_record'

    id: Mapped[int] = mapped_column(primary_key=True)
    staff_id: Mapped[str] = mapped_column(String(length=12))
    staff_name: Mapped[str] = mapped_column(String(length=64))
