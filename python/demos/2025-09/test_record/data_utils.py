"""
save JSON file to db

"""

import json
from typing import Any, Callable, List, Tuple

from sqlalchemy import create_engine, insert, text
from sqlalchemy.orm import Session
from test_record import PassFail, TestRecord

ENGINE = create_engine(
    "postgresql+psycopg://test1:test1@localhost:5432/demo1",
    connect_args={"options": "-c timezone=UTC", "connect_timeout": 3},
    echo=True,
)


UNSET = object()


def _convert_passfail(value):
    if value is UNSET:
        raise ValueError
    match value.upper():
        case "P":
            return PassFail.Pass
        case "F":
            return PassFail.Fail
        case "S":
            return PassFail.Start
        case _:
            return UNSET


"""
db key
json_file key.
default value when key not found from json file, 
additional function: value=func(value)

"""
KEY_MAPPING: List[Tuple[str, str, Any, Callable | None]] = [
    ("record_time", "rectime", UNSET, None),
    ("sernum", "sernum", UNSET, None),
    ("uuttype", "uuttype", UNSET, None),
    ("test_area", "area", UNSET, None),
    ("passfail", "passfail", UNSET, _convert_passfail),
    ("runtime", "attributes/RUNTIME", 0, None),
    ("test_fail", "attributes/TEST", "", None),
    ("test_machine", "machine", "", None),
    ("test_container", "attributes/CONTAINER", "", None),
    ("test_mode", "test_mode", "PROD0", None),
    ("deviation", "attributes/DEVIATION", "D000000", None),
    ("testr1name", "attributes/TESTR1NAME", None, None),
    ("testr1", "attributes/TESTR1", None, None),
    ("testr2name", "attributes/TESTR2NAME", None, None),
    ("testr2", "attributes/TESTR2", None, None),
    ("testr3name", "attributes/TESTR3NAME", None, None),
    ("testr3", "attributes/TESTR3", None, None),
]


def _get_value_from_hierarchy_keys(row_item: dict, key_string: str):
    new_keys = key_string.split("/")
    idx = 0
    while idx < len(new_keys) - 1:
        row_item = row_item.get(new_keys[idx], dict())
        idx += 1
    return row_item.get(new_keys[idx], UNSET)


def save_json_file_to_db(session: Session, filepath: str):
    with open(filepath, mode="r", encoding="utf8") as fp:
        row_data = json.load(fp)

    row_items = row_data["results"]["data"]
    print(f"total row items length is {len(row_items)}")
    data_to_insert = []

    for row_item in row_items:
        to_insert_item = {}

        for db_key, local_key, default_value, func in KEY_MAPPING:
            row_value = _get_value_from_hierarchy_keys(row_item, local_key)
            if row_value is UNSET:
                row_value = default_value
            if callable(func):
                row_value = func(row_value)
            to_insert_item[db_key] = row_value

        data_to_insert.append(to_insert_item)

    if not data_to_insert:
        print("noting to insert to db")
    else:
        stmt = insert(TestRecord)
        session.execute(stmt, data_to_insert)
        session.commit()
        print("insert local json data to db")


def call_pg_func_reflash_fp_flag(session: Session):
    func_name = "refresh_first_pass_flag"
    session.execute(
        text(f"SELECT {func_name}()"),
    )
    session.commit()


if __name__ == "__main__":
    """
    noting
    """
