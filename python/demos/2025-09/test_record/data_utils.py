"""
save JSON file to db

"""
import json
from typing import Any
from typing import List
from typing import Tuple

from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy.orm import Session

import schema
from schema import TestRecord

UNSET = object()

KEY_MAPPING: List[Tuple[str, str, Any]] = [
    ('tst_id', 'tst_id', UNSET),
    ('record_time', 'rectime', UNSET),
    ('sernum', 'sernum', UNSET),

    ('uuttype', 'uuttype', UNSET),
    ('test_area', 'area', UNSET),
    ('passfail', 'passfail', UNSET),
    ('runtime', 'attributes/RUNTIME', 0),
    ('test_fail', 'attributes/TEST', ''),
    ('test_machine', 'machine', ''),
    ('test_container', 'attributes/CONTAINER', ''),
    ('test_mode', 'test_mode', 'PROD0'),
    ('deviation', 'attributes/DEVIATION', 'D000000'),

    ('testr1name', 'attributes/TESTR1NAME', ''),
    ('testr1', 'attributes/TESTR1', ''),
    ('testr2name', 'attributes/TESTR2NAME', ''),
    ('testr2', 'attributes/TESTR2', ''),
    ('testr3name', 'attributes/TESTR3NAME', ''),
    ('testr3', 'attributes/TESTR3', ''),
]


def _get_hierarchy_value(row_item: dict, key_string: str):
    new_keys = key_string.split('/')
    idx = 0
    while idx < len(new_keys) - 1:
        row_item = row_item.get(new_keys[idx], dict())
        idx += 1
    return row_item.get(new_keys[idx], UNSET)


def save_json_file_to_db(filepath: str):
    # schema.create_tables()

    with open(filepath, mode='r', encoding='utf8') as fp:
        row_data = json.load(fp)

    row_items = row_data['results']['data']
    print(f'total row items length is {len(row_items)}')
    data_to_insert = []

    for row_item in row_items:
        to_insert_item = {}
        for db_key, local_key, action_or_default in KEY_MAPPING:
            if '/' in local_key:
                row_value = _get_hierarchy_value(row_item, local_key)
            else:
                row_value = row_item.get(local_key, UNSET)
            if row_value is UNSET:
                if callable(action_or_default):
                    row_value = action_or_default(row_value)
                else:
                    row_value = action_or_default
            to_insert_item[db_key] = row_value

        # copy first_pass_flag
        first_pass = row_item['firstpass']
        if first_pass:
            to_insert_item['first_pass_flag'] = schema.FirstPassState.FIRST
        else:
            to_insert_item['first_pass_flag'] = schema.FirstPassState.NOT_FIRST

        data_to_insert.append(to_insert_item)

    if not data_to_insert:
        print('noting to insert to db')
    else:
        stmt = insert(schema.TestRecord)
        with Session(schema.engine) as session:
            session.execute(stmt, data_to_insert)
            session.commit()
        print('insert local json data to db')


def get_processed_sernums(session: Session):
    """
    获取所有 first_pass_flag 不等于 -1 的 (sernum, test_area) 唯一组合
    对应 SQL:
    SELECT DISTINCT sernum, test_area
    FROM test_record
    WHERE first_pass_flag != -1
    """
    stmt = (
        select(TestRecord.sernum, TestRecord.test_area)
        .where(TestRecord.first_pass_flag != schema.FirstPassState.UNSET)
        .distinct()
    )

    result = session.execute(stmt).all()

    data_list = [(row.sernum, row.test_area) for row in result]
    return data_list


def update_first_pass_flags():
    """
    1. get tuple from (sernum, test_area)

    """
    session = Session(schema.engine)

    processed_list = get_processed_sernums(session)

    un_processed_stmt = (
        select(TestRecord).
        where(TestRecord.first_pass_flag == schema.FirstPassState.UNSET).
        order_by(TestRecord.record_time.asc())
    )
    un_processed_list = session.scalars(un_processed_stmt).all()
    for row in un_processed_list:
        _tuple = (row.sernum, row.test_area)
        if _tuple not in processed_list:
            first_pass_flag = schema.FirstPassState.FIRST
        else:
            first_pass_flag = schema.FirstPassState.NOT_FIRST
        row.first_pass_flag = first_pass_flag
        processed_list.append(_tuple)
        session.add(row)
    session.commit()


if __name__ == '__main__':
    pass
