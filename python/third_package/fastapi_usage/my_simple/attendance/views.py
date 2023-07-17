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
from . import utils
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
    records = db.query(models.AttendanceRecord). \
        order_by(models.AttendanceRecord.record_time). \
        all()
    return records


@router.get('/get/{staff_id}/', response_model=List[schemas.AttendanceRecord])
async def get_records_by_staff_id(staff_id: str, db: Session = Depends(get_db)):
    records = db.query(models.AttendanceRecord). \
        filter(models.AttendanceRecord.staff_id == staff_id). \
        order_by(models.AttendanceRecord.record_time). \
        all()
    return records


@router.post('/search/', response_model=List[schemas.AttendanceRecord])
async def search_records(params: schemas.SearchParams):
    """
    staff_id 可选

    record_type : 可选, in / out , 不选就是 in and out

    """
    print(params)
    if params.staff_id and not utils.is_valid_staff_id(params.staff_id):
        raise HTTPException(status_code=400, detail='not valid staff id')

    if params.record_type and not models.is_valid_record_type(params.record_type):
        raise HTTPException(status_code=400,
                            detail='record type is not valid, must be "in" or "out"')

    return []
