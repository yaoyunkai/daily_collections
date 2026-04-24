"""
employee_punch.py


created at 2026-04-24
"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, time
from enum import Enum
from typing import List, Set, Tuple


class MachineType(Enum):
    IN = "入"
    OUT = "出"


class AttendStatus(Enum):
    NORMAL = "正常"
    LATE = "迟到"
    EARLY_LEAVE = "早退"
    ABSENT = "旷工"
    MISSING_PUNCH = "缺卡/打卡异常"
    OUTING_TIMEOUT = "外出超时(>2小时)"
    OUTING_CROSS_LUNCH = "外出违规(跨午休)"


@dataclass
class ShiftRule:
    """班别规则"""

    start_time: time
    end_time: time
    lunch_start: time
    lunch_end: time


@dataclass
class PunchRecord:
    """打卡记录"""

    emp_id: str
    timestamp: datetime
    machine_type: MachineType


@dataclass
class DailyResult:
    """每日考勤计算结果"""

    date: str
    effective_hours: float
    status: Set[AttendStatus]
    details: str


# --- 2. 核心算法 ---


def _pair_punches(punches: List[PunchRecord]) -> Tuple[List[Tuple[datetime, datetime]], bool]:
    """将当天的打卡记录清洗并配对为 (入, 出) 时间段"""
    punches.sort(key=lambda x: x.timestamp)
    intervals = []
    current_in = None
    is_missing_punch = False

    for punch in punches:
        if punch.machine_type == MachineType.IN:
            if current_in is None:
                current_in = punch.timestamp
        elif punch.machine_type == MachineType.OUT:
            if current_in is not None:
                intervals.append((current_in, punch.timestamp))
                current_in = None
            else:
                if intervals:
                    intervals[-1] = (intervals[-1][0], punch.timestamp)
                else:
                    is_missing_punch = True

    if current_in is not None:
        is_missing_punch = True

    return intervals, is_missing_punch


def _get_overlap_seconds(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> float:
    """计算两个时间段重叠的秒数"""
    overlap_start = max(start1, start2)
    overlap_end = min(end1, end2)
    if overlap_end > overlap_start:
        return (overlap_end - overlap_start).total_seconds()
    return 0.0


def calculate_attendance(records: List[PunchRecord], _rule: ShiftRule) -> dict[str, DailyResult]:
    """主计算逻辑"""
    daily_records = defaultdict(list)
    for r in records:
        date_str = r.timestamp.date().isoformat()
        daily_records[date_str].append(r)

    _results = {}

    for date_str, punches in daily_records.items():
        current_date = datetime.fromisoformat(date_str).date()

        # 1. 记录清洗与配对
        intervals, is_missing_punch = _pair_punches(punches)
        statuses = set()

        dt_start = datetime.combine(current_date, _rule.start_time)
        dt_end = datetime.combine(current_date, _rule.end_time)
        dt_lunch_start = datetime.combine(current_date, _rule.lunch_start)
        dt_lunch_end = datetime.combine(current_date, _rule.lunch_end)

        work_period_1 = (dt_start, dt_lunch_start)
        work_period_2 = (dt_lunch_end, dt_end)

        if not intervals:
            statuses.add(AttendStatus.MISSING_PUNCH if is_missing_punch else AttendStatus.ABSENT)
            _results[date_str] = DailyResult(date_str, 0.0, statuses, "无有效打卡区间")
            continue

        if is_missing_punch:
            statuses.add(AttendStatus.MISSING_PUNCH)

        # 2. 迟到与早退判断 (基于最原始的最早入和最晚出)
        if intervals[0][0] > dt_start:
            statuses.add(AttendStatus.LATE)
        if intervals[-1][1] < dt_end and not is_missing_punch:
            statuses.add(AttendStatus.EARLY_LEAVE)

        # 3. 外出规则判定与区间合并 (核心修改点)
        merged_intervals = [intervals[0]]

        for i in range(1, len(intervals)):
            prev_in, prev_out = merged_intervals[-1]
            next_in, next_out = intervals[i]

            gap_start = prev_out
            gap_end = next_in
            gap_duration = (gap_end - gap_start).total_seconds()

            # 判断 Gap 的性质
            is_pure_lunch = gap_start >= dt_lunch_start and gap_end <= dt_lunch_end
            crosses_lunch = gap_start < dt_lunch_start and gap_end > dt_lunch_end
            is_timeout = gap_duration > 2 * 3600

            if is_pure_lunch:
                # 正常午休打卡，合并区间（后续交集计算会自动扣除午休时间）
                merged_intervals[-1] = (prev_in, next_out)
            elif crosses_lunch:
                # 违规：跨午休，不合并区间（扣除工时）
                statuses.add(AttendStatus.OUTING_CROSS_LUNCH)
                merged_intervals.append((next_in, next_out))
            elif is_timeout:
                # 违规：超时，不合并区间（扣除工时）
                statuses.add(AttendStatus.OUTING_TIMEOUT)
                merged_intervals.append((next_in, next_out))
            else:
                # 正常外出：<=2小时且不跨午休，合并区间（视同在岗，不扣工时）
                merged_intervals[-1] = (prev_in, next_out)

        # 4. 有效工时计算 (使用合并后的区间与规定工作区间求交集)
        total_effective_seconds = 0.0
        for actual_in, actual_out in merged_intervals:
            total_effective_seconds += _get_overlap_seconds(actual_in, actual_out, *work_period_1)
            total_effective_seconds += _get_overlap_seconds(actual_in, actual_out, *work_period_2)

        effective_hours = total_effective_seconds / 3600.0

        if not statuses:
            statuses.add(AttendStatus.NORMAL)

        _results[date_str] = DailyResult(
            date=date_str,
            effective_hours=round(effective_hours, 2),
            status=statuses,
            details=f"原始区间数: {len(intervals)} -> 合并后区间数: {len(merged_intervals)}",
        )

    return _results


# --- 3. Dummy 数据模拟与测试 ---

if __name__ == "__main__":
    rule = ShiftRule(start_time=time(9, 0), end_time=time(18, 0), lunch_start=time(12, 0), lunch_end=time(13, 0))

    dummy_records = [
        # 场景 1: 正常，无午休打卡 -> 预期 8小时，正常
        PunchRecord("E01", datetime(2023, 11, 1, 8, 50), MachineType.IN),
        PunchRecord("E01", datetime(2023, 11, 1, 18, 5), MachineType.OUT),
        # 场景 2: 正常，有午休打卡 -> 预期 8小时，正常
        PunchRecord("E01", datetime(2023, 11, 2, 8, 55), MachineType.IN),
        PunchRecord("E01", datetime(2023, 11, 2, 12, 0), MachineType.OUT),
        PunchRecord("E01", datetime(2023, 11, 2, 12, 55), MachineType.IN),
        PunchRecord("E01", datetime(2023, 11, 2, 18, 10), MachineType.OUT),
        # 场景 3: 临时外出正常 (上午外出1小时，10:00-11:00)
        # -> 【变更】预期 8小时 (正常外出不扣工时)，正常
        PunchRecord("E01", datetime(2023, 11, 4, 8, 50), MachineType.IN),
        PunchRecord("E01", datetime(2023, 11, 4, 10, 0), MachineType.OUT),
        PunchRecord("E01", datetime(2023, 11, 4, 11, 0), MachineType.IN),
        PunchRecord("E01", datetime(2023, 11, 4, 18, 0), MachineType.OUT),
        # 场景 4: 外出超时 (下午外出2.5小时，14:00-16:30)
        # -> 预期 5.5小时 (违规外出，扣除2.5小时)，外出超时
        PunchRecord("E01", datetime(2023, 11, 5, 8, 50), MachineType.IN),
        PunchRecord("E01", datetime(2023, 11, 5, 14, 0), MachineType.OUT),
        PunchRecord("E01", datetime(2023, 11, 5, 16, 30), MachineType.IN),
        PunchRecord("E01", datetime(2023, 11, 5, 18, 0), MachineType.OUT),
        # 场景 5: 外出跨午休违规 (11:30 - 13:30)
        # -> 预期 7小时 (违规外出，扣除工作时间内的1小时)，外出跨午休
        PunchRecord("E01", datetime(2023, 11, 6, 8, 50), MachineType.IN),
        PunchRecord("E01", datetime(2023, 11, 6, 11, 30), MachineType.OUT),
        PunchRecord("E01", datetime(2023, 11, 6, 13, 30), MachineType.IN),
        PunchRecord("E01", datetime(2023, 11, 6, 18, 0), MachineType.OUT),
    ]

    results = calculate_attendance(dummy_records, rule)

    print(f"班别规则: 上班 {rule.start_time}-{rule.end_time} | 午休 {rule.lunch_start}-{rule.lunch_end}\n")
    print("-" * 80)
    for date, res in sorted(results.items()):
        status_strs = [s.value for s in res.status]
        print(f"日期: {date} | 工时: {res.effective_hours:>4}h | 状态: {', '.join(status_strs):<15} | {res.details}")
    print("-" * 80)
