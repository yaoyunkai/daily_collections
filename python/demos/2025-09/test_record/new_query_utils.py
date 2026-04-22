"""
new_query_utils.py


get_test_record_by_sernum


created at 2026-04-15
"""

from datetime import date, datetime
from enum import Enum
from typing import Annotated, Optional

import pandas as pd
import pendulum
from data_utils import ENGINE  # noqa: F401
from pydantic import BaseModel, BeforeValidator, ConfigDict, field_validator, model_validator
from QueryExpr.runner import QMode, parse_query
from sqlalchemy import Select, or_, select
from sqlalchemy.orm import Session
from test_record import PassFail, TestRecord

MAX_LIMIT = 5000


class DataType(Enum):
    TEST = "test"
    FIRST_PASS = "first_pass"


class ViewType(Enum):
    NO_DATE = "no_date"
    WEEK = "week"
    MONTH = "month"


def _convert_param_str(param_str: str):
    return parse_query(param_str)


ParamQueryList = Annotated[Optional[list[tuple[QMode, str]]], BeforeValidator(_convert_param_str)]


class YieldSearchIn(BaseModel):
    sernum: ParamQueryList = None
    uuttype: ParamQueryList = None
    test_machine: ParamQueryList = None
    test_area: ParamQueryList = None

    start_date: date
    end_date: date
    data_type: DataType = DataType.TEST

    view_type: ViewType = ViewType.NO_DATE

    @model_validator(mode="after")
    def validate_cross_fields(self):
        if not any([self.sernum, self.uuttype, self.test_machine, self.test_area]):
            raise ValueError(
                "Must provide at least one search parameter: 'sernum', 'uuttype', 'test_machine', or 'test_area'."
            )
        if self.start_date > self.end_date:
            raise ValueError("'start_date' cannot be >= 'end_date'.")

        return self


class MultiSearchIn(BaseModel):
    sernum: ParamQueryList = None
    uuttype: ParamQueryList = None
    test_machine: ParamQueryList = None
    test_area: ParamQueryList = None

    start_date: date
    end_date: date
    data_type: DataType = DataType.TEST

    # must select one of below include_
    include_pass: bool = True
    include_fail: bool = True
    include_start: bool = True

    @model_validator(mode="after")
    def validate_cross_fields(self):
        if not any([self.sernum, self.uuttype, self.test_machine, self.test_area]):
            raise ValueError(
                "Must provide at least one search parameter: 'sernum', 'uuttype', 'test_machine', or 'test_area'."
            )

        if self.start_date > self.end_date:
            raise ValueError("'start_date' cannot be >= 'end_date'.")

        if not any([self.include_pass, self.include_fail, self.include_start]):
            raise ValueError("At least one of 'include_pass', 'include_fail', or 'include_start' must be True.")

        return self


class YieldMetrics(BaseModel):
    pass_qty: int = 0
    fail_qty: int = 0
    total_qty: int = 0
    pass_rate: str = "0.00%"


class YieldRowOut(BaseModel):
    date_group: Optional[str] = None  # 新增：用于显示 Week 或 Month
    uuttype: str
    avg_yield: str
    board_qty: int
    ete_yield: Optional[YieldMetrics] = None
    areas: dict[str, YieldMetrics]


class TestRecordOut(BaseModel):
    record_time: datetime
    sernum: str
    uuttype: str
    test_area: str
    passfail: str
    runtime: int
    test_fail: str
    test_machine: str
    test_container: str
    first_pass_flag: bool | None

    # 允许 Pydantic 从 SQLAlchemy 的 Row 或 ORM 对象中读取数据
    model_config = ConfigDict(from_attributes=True)

    @field_validator("passfail", mode="before")
    @classmethod
    def convert_passfail(cls, value) -> str:
        val_str = value.value if hasattr(value, "value") else str(value)
        mapping = {"pass": "P", "fail": "F", "start": "S"}
        return mapping.get(val_str.lower(), val_str)


class Querying(object):
    S_All = "All"
    S_Summary = "ZZZ_Summary"

    def __init__(self, engine):
        self.session = Session(engine)

    def get_test_record_by_sernum(self, sernum: str):
        stmt = (
            select(TestRecord)
            .where(TestRecord.sernum == sernum)
            .order_by(TestRecord.record_time.asc())
            .limit(MAX_LIMIT)
        )
        rows = self.session.scalars(stmt).all()

        return [TestRecordOut.model_validate(row) for row in rows]

    def multi_search_test_record(self, search_params: dict, *, max_rows=MAX_LIMIT):
        validated_params = MultiSearchIn.model_validate(search_params)

        stmt = select(TestRecord)
        stmt = self._make_common_params_stmt(stmt, validated_params)

        passfail_conditions = [
            (validated_params.include_pass, PassFail.Pass),
            (validated_params.include_fail, PassFail.Fail),
            (validated_params.include_start, PassFail.Start),
        ]
        passfail_list = [pf_enum for is_included, pf_enum in passfail_conditions if is_included]

        stmt = stmt.where(TestRecord.passfail.in_(passfail_list)).order_by(TestRecord.record_time.asc()).limit(max_rows)

        rows = self.session.scalars(stmt).all()
        return [TestRecordOut.model_validate(row) for row in rows]

    def get_yield_report_pandas(self, search_params: dict) -> list[YieldRowOut]:
        """
        另一个方式: 三份数据（原数据、时间段汇总数据、全局汇总数据）

        """
        validated_params = YieldSearchIn.model_validate(search_params)

        stmt = select(
            TestRecord.uuttype,
            TestRecord.sernum,
            TestRecord.test_area,
            TestRecord.passfail,
            TestRecord.record_time,
        )
        stmt = self._make_common_params_stmt(stmt, validated_params)
        stmt = stmt.where(TestRecord.passfail.in_([PassFail.Pass, PassFail.Fail]))

        df = pd.read_sql(stmt, self.session.bind)

        if df.empty:
            return []

        df["passfail"] = df["passfail"].apply(lambda x: x.value if hasattr(x, "value") else str(x)).str.lower()
        df["is_pass"] = (df["passfail"] == "pass").astype(int)

        # 处理 view_type (生成 date_group 列)
        if validated_params.view_type is ViewType.WEEK:
            df["date_group"] = df["record_time"].dt.strftime("%G-W%V")
        elif validated_params.view_type is ViewType.MONTH:
            df["date_group"] = df["record_time"].dt.strftime("%Y-%m")
        else:
            df["date_group"] = self.S_All

        is_first_pass = validated_params.data_type is DataType.FIRST_PASS

        # ==========================================
        # 步骤 A: 基础数据统计 (按 date_group + uuttype)
        # ==========================================
        base_stats = (
            df.groupby(["date_group", "uuttype"])
            .agg(
                board_qty=("sernum", "nunique"),
                total_tests=("is_pass", "count"),
                total_pass=("is_pass", "sum"),
            )
            .reset_index()
        )

        base_stats_area = (
            df.groupby(["date_group", "uuttype", "test_area"])
            .agg(
                total_qty=("is_pass", "count"),
                pass_qty=("is_pass", "sum"),
            )
            .reset_index()
        )

        # ==========================================
        # 步骤 B: 全局汇总统计 (Grand Total，不按任何维度分组)
        # ==========================================
        # 整体基础统计
        gs_stats = pd.DataFrame(
            [
                {
                    "date_group": "Total",
                    "uuttype": self.S_Summary,
                    "board_qty": df["sernum"].nunique(),
                    "total_tests": len(df),
                    "total_pass": df["is_pass"].sum(),
                }
            ]
        )

        # 整体工站统计 (仅按 test_area 分组)
        gs_stats_area = (
            df.groupby(["test_area"])
            .agg(
                total_qty=("is_pass", "count"),
                pass_qty=("is_pass", "sum"),
            )
            .reset_index()
        )
        gs_stats_area["date_group"] = "Total"
        gs_stats_area["uuttype"] = self.S_Summary

        stats_list = [base_stats, gs_stats]
        area_list = [base_stats_area, gs_stats_area]
        ete_list = []

        if is_first_pass:
            _base_sernum_ete = df.groupby(["date_group", "uuttype", "sernum"])["is_pass"].min().reset_index()
            base_ete = (
                _base_sernum_ete.groupby(["date_group", "uuttype"])
                .agg(
                    ete_total=("is_pass", "count"),
                    ete_pass=("is_pass", "sum"),
                )
                .reset_index()
            )
            ete_list.append(base_ete)

            # 整体 ETE 统计 (仅按 sernum 判断)
            _gs_sernum_ete = df.groupby("sernum")["is_pass"].min().reset_index()
            gs_ete = pd.DataFrame(
                [
                    {
                        "date_group": "Total",
                        "uuttype": self.S_Summary,
                        "ete_total": len(_gs_sernum_ete),
                        "ete_pass": _gs_sernum_ete["is_pass"].sum(),
                    }
                ]
            )
            ete_list.append(gs_ete)

        # ==========================================
        # 步骤 C: 合并统计结果
        # ==========================================
        final_stats = pd.concat(stats_list, ignore_index=True)
        final_stats_area = pd.concat(area_list, ignore_index=True)

        # print(final_stats)
        # print(final_stats_area)

        # 将工站数据转为嵌套字典以供快速查询: {(date_group, uuttype): {test_area: metrics}}
        area_dict = (
            final_stats_area.groupby(["date_group", "uuttype"])
            .apply(lambda x: x.set_index("test_area").to_dict("index"))
            .to_dict()
        )

        ete_dict = {}
        if is_first_pass:
            final_ete = pd.concat(ete_list, ignore_index=True)
            ete_dict = final_ete.set_index(["date_group", "uuttype"]).to_dict("index")

        # ==========================================
        # 步骤 D: 组装 Pydantic 输出
        # ==========================================
        report_rows = []
        for _, row in final_stats.iterrows():
            dg = row["date_group"]
            uut = row["uuttype"]

            # Avg Yield
            t_tests = row["total_tests"]
            avg_rate = f"{(row['total_pass'] / t_tests * 100):.2f}%" if t_tests > 0 else "0.00%"

            # Test Area Metrics
            areas_metrics = {}
            if (dg, uut) in area_dict:
                for area, stats in area_dict[(dg, uut)].items():
                    p_qty = stats["pass_qty"]
                    t_qty = stats["total_qty"]
                    f_qty = t_qty - p_qty
                    rate = f"{(p_qty / t_qty * 100):.2f}%" if t_qty > 0 else "0.00%"
                    areas_metrics[area] = YieldMetrics(pass_qty=p_qty, fail_qty=f_qty, total_qty=t_qty, pass_rate=rate)

            # ETE Yield
            ete_metrics = None
            if is_first_pass and (dg, uut) in ete_dict:
                e_pass = ete_dict[(dg, uut)]["ete_pass"]
                e_total = ete_dict[(dg, uut)]["ete_total"]
                e_fail = e_total - e_pass
                e_rate = f"{(e_pass / e_total * 100):.2f}%" if e_total > 0 else "0.00%"
                ete_metrics = YieldMetrics(pass_qty=e_pass, fail_qty=e_fail, total_qty=e_total, pass_rate=e_rate)

            # 如果是 NO_DATE 模式，输出时隐藏 date_group
            display_dg = dg if validated_params.view_type is not ViewType.NO_DATE else None

            report_rows.append(
                YieldRowOut(
                    date_group=display_dg,
                    uuttype=uut,
                    avg_yield=avg_rate,
                    board_qty=row["board_qty"],
                    ete_yield=ete_metrics,
                    areas=areas_metrics,
                )
            )

        # 排序输出：保证 Total 永远在最后一行
        # def sort_key(x):
        #     # 内部使用 'Total' 作为标识，排序时将其置于最后
        #     dg_order = "ZZZZZ" if x.date_group == "Total" else (x.date_group or "")
        #     uut_order = "ZZZZZ" if x.uuttype == "Summary" else x.uuttype
        #     return dg_order, uut_order
        #
        # report_rows.sort(key=sort_key)
        return report_rows

    @classmethod
    def _make_common_params_stmt(cls, stmt: "Select", search_object: MultiSearchIn | YieldSearchIn):
        common_query_list = ["sernum", "uuttype", "test_machine", "test_area"]

        for param_name in common_query_list:
            query_data_list: list[tuple[QMode, str]] = getattr(search_object, param_name)
            if not query_data_list:
                continue

            orm_filed_obj = getattr(TestRecord, param_name)

            _or_list = []
            for query_mode, query_str in query_data_list:
                if query_mode is QMode.Normal:
                    _or_list.append(orm_filed_obj == query_str)
                if query_mode is QMode.Pattern:
                    _or_list.append(orm_filed_obj.like(query_str))

            if len(_or_list) == 0:
                continue

            stmt = stmt.where(or_(*_or_list))
            _or_list.clear()

        start_date = search_object.start_date
        start_date = pendulum.datetime(start_date.year, start_date.month, start_date.day)
        end_date = search_object.end_date
        end_date = pendulum.datetime(end_date.year, end_date.month, end_date.day).add(days=1)

        stmt = stmt.where(
            TestRecord.record_time >= start_date,
            TestRecord.record_time < end_date,
        )

        if search_object.data_type is DataType.FIRST_PASS:
            stmt = stmt.where(TestRecord.first_pass_flag == True)  # noqa: E712

        return stmt


if __name__ == "__main__":
    pass
