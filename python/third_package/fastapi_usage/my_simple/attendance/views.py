"""

response_model用于定义响应的数据结构并执行验证，
response_class用于自定义响应的格式和发送回客户端的方式。


Created at 2023/7/15
"""
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import crud
from . import models
from . import schemas
from ..database import get_db

router = APIRouter(
    tags=['Attendance']
)


@router.post("/create/", response_model=schemas.AttendanceRecord)
async def create_record(record: schemas.AttendanceRecordBase, db: Session = Depends(get_db)):
    if not models.is_valid_record_type(record.record_type):
        raise HTTPException(status_code=400,
                            detail='record type is not valid, must be "in" or "out"')
    return crud.create_record(db=db, record=record)


@router.get('/get/', response_model=List[schemas.AttendanceRecord])
async def get_all_records(db: Session = Depends(get_db)):
    records = db.query(models.AttendanceRecord).all()
    return records


@router.get('/get/{staff_id}/', response_model=List[schemas.AttendanceRecord])
async def get_record_by_staff_id(staff_id: str, db: Session = Depends(get_db)):
    records = db.query(models.AttendanceRecord).filter(models.AttendanceRecord.staff_id == staff_id).all()
    return records
