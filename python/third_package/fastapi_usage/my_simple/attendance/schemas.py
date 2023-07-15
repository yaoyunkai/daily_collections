"""


Created at 2023/7/15
"""
import datetime

from pydantic import BaseModel


class AttendanceRecordBase(BaseModel):
    """
    also use as create function

    """
    staff_id: str
    staff_name: str

    record_time: datetime.datetime
    record_machine: str
    record_type: str


class AttendanceRecord(AttendanceRecordBase):
    id: int

    class Config:
        orm_mode = True
