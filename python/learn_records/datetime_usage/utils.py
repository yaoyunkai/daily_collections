"""
utils.py


object
    timedelta
    tzinfo
        timezone
    time
    date
        datetime


==================================================
ISO 8601 格式 / datetime_obj.isoformat()
    2023-10-27T15:30:00Z
    2023-10-27T23:30:00+08:00

RFC 2822 / RFC 3339
    Fri, 27 Oct 2023 15:30:00 +0800


created at 2026-04-09
"""

import re
from datetime import datetime, timedelta, timezone
from functools import lru_cache


def is_aware(dt: datetime) -> bool:
    """判断 datetime 对象是否包含时区信息 (Aware)"""
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None


@lru_cache()
def get_local_tz():
    """
    获取本地的时区

    """
    local_tz = datetime.now().astimezone().tzinfo
    return local_tz


def get_utc_current():
    """
    获取当前的UTC时间

    """
    return datetime.now(tz=timezone.utc)


def get_local_current():
    """
    获取本地时间，无时区
    """
    return datetime.now()


def create_datetime_with_tz(year, month, day, hour, minute, second, *, tz=None):
    """
    创建带时区的时间，默认为UTC时区的时间

    """
    if tz is None:
        tz = timezone.utc

    return datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        tzinfo=tz,
    )


def create_datetime_without_tz(year, month, day, hour, minute, second):
    return datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        tzinfo=None,
    )


def to_tz_datetime(dt_obj: datetime) -> datetime:
    """
    转换为带本地时区的时间 (Aware)。

    推理逻辑：
    1. 如果已经有时区，直接转换为本地时区 (处理跨时区转换)。
    2. 如果没有时区，我们假设这个时间在字面上已经是本地时间，
       仅仅为它“贴上”本地时区的标签，而不改变它的字面数值。
    """
    local_tz = get_local_tz()

    if is_aware(dt_obj):
        # 如果传入的是其他时区(如UTC)，安全地计算时差并转为本地时区
        return dt_obj.astimezone(local_tz)

    # 如果是 Naive，千万不要用 astimezone！
    # 使用 replace 直接贴上标签，保证字面时间不变 (例如 12:00 依然是 12:00)
    return dt_obj.replace(tzinfo=local_tz)


def to_non_tz_datetime(dt_obj: datetime) -> datetime:
    """
    转换为不带时区的时间 (Naive)，且其字面数值代表 UTC 时间。

    推理逻辑：
    1. 如果有时区，先转为 UTC，再撕掉标签。
    2. 如果没有时区，我们必须假设它原本代表什么。通常在 Web 后端，
       如果产生了一个 Naive 时间，大概率是系统本地时间 (如 datetime.now())。
       因此我们先将其视为本地时间，转为 UTC，再撕掉标签。
    """
    if is_aware(dt_obj):
        return dt_obj.astimezone(timezone.utc).replace(tzinfo=None)

    # 如果是 Naive 时间，为了安全起见：
    # 1. 先把它当作本地时间贴上标签 (变成 Aware)
    # 2. 转为 UTC 时间
    # 3. 撕掉标签
    local_tz = get_local_tz()
    dt_aware_local = dt_obj.replace(tzinfo=local_tz)
    dt_utc_naive = dt_aware_local.astimezone(timezone.utc).replace(tzinfo=None)

    return dt_utc_naive


def parse_datetime(iso_str: str) -> datetime:
    try:
        return datetime.fromisoformat(iso_str)
    except Exception:
        raise ValueError(f"error when parse iso datetime string with '{iso_str}'")


def parse_iso8601_datetime(iso_str: str) -> datetime:
    """
    使用正则表达式解析 ISO 8601 字符串并返回 datetime 对象。
    """
    iso8601_pattern = re.compile(
        r"^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})"
        r"[T\s]"
        r"(?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<second>\d{1,2})"
        r"(?:\.(?P<fraction>\d+))?"
        r"(?P<tz>Z|[+-]\d{2}:?(?:\d{2})?)?$"
    )

    match = iso8601_pattern.match(iso_str)
    if not match:
        raise ValueError(f"字符串 '{iso_str}' 不符合 ISO 8601 格式")

    groups = match.groupdict()

    year = int(groups["year"])
    month = int(groups["month"])
    day = int(groups["day"])
    hour = int(groups["hour"])
    minute = int(groups["minute"])
    second = int(groups["second"])

    microsecond = 0
    if groups["fraction"]:
        fraction_str = groups["fraction"].ljust(6, "0")[:6]
        microsecond = int(fraction_str)

    tzinfo = None
    tz_str = groups["tz"]
    if tz_str:
        if tz_str.upper() == "Z":
            tzinfo = timezone.utc
        else:
            # 解析 +HH:MM, -HH:MM, +HHMM 等格式
            sign = 1 if tz_str.startswith("+") else -1
            # 移除符号和冒号，只保留数字
            tz_clean = tz_str[1:].replace(":", "")
            tz_hour = int(tz_clean[:2])
            tz_minute = int(tz_clean[2:]) if len(tz_clean) >= 4 else 0

            # 计算偏移量
            offset = timedelta(hours=tz_hour, minutes=tz_minute) * sign
            tzinfo = timezone(offset)

    return datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        microsecond=microsecond,
        tzinfo=tzinfo,
    )


if __name__ == "__main__":
    pass
