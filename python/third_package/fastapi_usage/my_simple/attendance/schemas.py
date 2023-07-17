"""


Created at 2023/7/15
"""
import datetime
from typing import Optional

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


class SearchParams(BaseModel):
    """
    for search_records

    """

    staff_id: Optional[str]
    record_type: Optional[str]

    start_time: str
    end_time: Optional[str]
