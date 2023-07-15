"""


Created at 2023/7/15
"""

from sqlalchemy.orm import Session

from . import models
from . import schemas


def create_record(db: Session, record: schemas.AttendanceRecordBase) -> models.AttendanceRecord:
    db_record = models.AttendanceRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
