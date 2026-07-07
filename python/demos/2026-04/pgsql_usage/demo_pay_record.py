"""
demo1.py



created at 2026-07-03
"""

import enum
import random
import uuid
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import DateTime, Integer, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

engine = create_engine(
    "postgresql+psycopg://test1:test1@localhost:5432/demo1",
    connect_args={"options": "-c timezone=UTC", "connect_timeout": 3},
    echo=True,
)

LOCAL_TZ = ZoneInfo("Asia/Shanghai")


class TimeRangeType(enum.Enum):
    Today = "today"
    ThisMonth = "this_month"
    Last7Days = "last_7_days"
    Last30Days = "last_30_days"


class Base(DeclarativeBase):
    pass


class PayRecord(Base):
    __tablename__ = "demo_pay_record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[str] = mapped_column(String(32), nullable=False)
    amount: Mapped[int] = mapped_column(Integer)
    pay_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


def generate_mock_pay_records(msession: Session):
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=90)

    user_pool = []

    records_to_insert = []

    current_date = start_date
    while current_date <= end_date:
        daily_orders = random.randint(550, 650)

        for _ in range(daily_orders):
            if not user_pool or random.random() < 0.4:
                user_id = uuid.uuid4().hex
                user_pool.append(user_id)
            else:
                user_id = random.choice(user_pool)

            amount = random.randint(10, 80)

            is_lunch = random.random() < 0.5
            if is_lunch:
                hour = random.randint(11, 13)
            else:
                hour = random.randint(17, 21)

            minute = random.randint(0, 59)
            second = random.randint(0, 59)

            pay_at = datetime(
                year=current_date.year,
                month=current_date.month,
                day=current_date.day,
                hour=hour,
                minute=minute,
                second=second,
                tzinfo=timezone.utc,
            )

            record = PayRecord(user_id=user_id, amount=amount, pay_at=pay_at, created_at=pay_at)
            records_to_insert.append(record)

        current_date += timedelta(days=1)

        if len(records_to_insert) >= 5000:
            msession.bulk_save_objects(records_to_insert)
            msession.commit()
            records_to_insert.clear()

    if records_to_insert:
        msession.bulk_save_objects(records_to_insert)
        msession.commit()

    print("模拟数据生成完毕！")


def get_time_range(range_type: TimeRangeType, tz_info: ZoneInfo = LOCAL_TZ) -> tuple[datetime, datetime]:
    """
    获取指定时间范围的起点和终点 (左闭右开: >= start, < end)

    """
    date_now = datetime.now(tz_info)
    today_start = datetime(date_now.year, date_now.month, date_now.day, tzinfo=tz_info)
    tomorrow_start = today_start + timedelta(days=1)

    if range_type is TimeRangeType.Today:
        return today_start, tomorrow_start

    elif range_type is TimeRangeType.ThisMonth:
        month_start = datetime(date_now.year, date_now.month, 1, tzinfo=tz_info)
        if date_now.month == 12:
            next_month_start = datetime(date_now.year + 1, 1, 1, tzinfo=tz_info)
        else:
            next_month_start = datetime(date_now.year, date_now.month + 1, 1, tzinfo=tz_info)
        return month_start, next_month_start

    elif range_type is TimeRangeType.Last7Days:
        start = today_start - timedelta(days=6)
        return start, tomorrow_start

    elif range_type is TimeRangeType.Last30Days:
        start = today_start - timedelta(days=29)
        return start, tomorrow_start

    else:
        raise ValueError(f"不支持的时间范围类型: {range_type}")


def get_today_sales_amount(msession: Session) -> int:
    start_of_today, start_of_tomorrow = get_time_range(TimeRangeType.Today)

    stmt = (
        select(func.sum(PayRecord.amount))
        .where(PayRecord.pay_at >= start_of_today)
        .where(PayRecord.pay_at < start_of_tomorrow)
    )
    total_amount = msession.scalar(stmt) or 0
    return total_amount


def get_this_month_sales_amount(msession: Session) -> int:
    start_of_today, start_of_tomorrow = get_time_range(TimeRangeType.ThisMonth)

    stmt = (
        select(func.sum(PayRecord.amount))
        .where(PayRecord.pay_at >= start_of_today)
        .where(PayRecord.pay_at < start_of_tomorrow)
    )
    total_amount = msession.scalar(stmt) or 0
    return total_amount


if __name__ == "__main__":
    pass
