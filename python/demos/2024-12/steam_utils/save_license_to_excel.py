"""
获取steam license的历史记录，转换为

将下面的网址的内容粘贴到 excel 即可
https://store.steampowered.com/account/licenses/


"""
import re
from datetime import date, datetime
from enum import Enum, auto

import openpyxl
import pandas
from openpyxl.cell import MergedCell

# BASE_DIR = r'C:\Users\10524\Downloads'
LICENSE_FILE = r"C:\Users\10524\Downloads\steam 产品序列号.xlsx"


class LicenseType(Enum):
    FREE = auto()
    STEAM_STORE = auto()
    CDK = auto()
    GIFT = auto()


def get_current_datetime():
    _obj = datetime.now()
    return _obj.strftime('%Y%m%d%H%M%S')


def normalize_datetime(val: str):
    """
    2024 年 11 月 28 日


    :param val:
    :return:
    """
    pattern = re.compile(r'(\d{4}) 年 (\d{1,2}) 月 (\d{1,2}) 日')

    match = pattern.search(val)
    if not match:
        raise ValueError('not format value')

    return date(*[int(s) for s in match.groups()])


def convert_license_type(val: str):
    if '商店' in val:
        return LicenseType.STEAM_STORE
    if '免费' in val:
        return LicenseType.FREE
    if '零售' in val:
        return LicenseType.CDK
    if '礼物' in val:
        return LicenseType.GIFT


def get_license_list(filename: str):
    wb = openpyxl.load_workbook(filename)
    work_sheet = wb.worksheets[0]

    result_list = []

    for idx, row in enumerate(work_sheet.iter_rows(min_row=2, max_col=3)):
        date_str_col, item_name_col, license_type_col = row

        if isinstance(date_str_col, MergedCell):
            last_item = result_list[-1]
            last_item[1] = item_name_col.value

        else:
            item = [
                normalize_datetime(date_str_col.value),
                item_name_col.value,
                license_type_col.value,
            ]
            result_list.append(item)

    print(f'获取了{len(result_list)}条数据')

    return result_list


def save_steam_license_file_to_excel(license_list: list):
    filename = 'steam_license_{}.xlsx'.format(get_current_datetime())

    df = pandas.DataFrame(license_list, columns=['date', 'item_name', 'license_type'])

    df['date'] = pandas.to_datetime(df['date'])
    # df['item_name'] = df['item_name'].astype(str)
    # df['license_type'] = df['license_type'].astype(str)

    df.to_excel(filename, index=False)


if __name__ == '__main__':
    get_license_list(LICENSE_FILE)
