"""


Created at 2023/4/17
"""
import datetime
import json
import os.path

import openpyxl
from openpyxl.styles import Border, Font, PatternFill, Side


def read_from_history(filename):
    filepath = os.path.join('history', filename)

    fp = open(filepath, mode='r', encoding='utf8')
    data = json.load(fp)
    fp.close()
    return data


def read_last_history():
    file_lists = os.listdir('history')

    file_lists.sort()
    return read_from_history(file_lists[-1])


def save_test_record_to_excel(test_records):
    date_now = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

    _data_results = []

    if not test_records:
        return

    _data_results.append(
        ['record time', 'sernum', 'uuttype', 'area',
         'passfail', 'test failure', 'server',
         'container', 'gb_sn', 'gb_pn']
    )

    for test_item in test_records:
        _data_items = []

        record_time = test_item['rectime']
        record_time = record_time.replace('.000', '')
        _data_items.append(record_time)

        sernum = test_item['sernum']
        _data_items.append(sernum)

        uuttype = test_item['uuttype']
        _data_items.append(uuttype)

        area = test_item['area']
        _data_items.append(area)

        passfail = test_item['passfail']
        _data_items.append(passfail)

        test_failure = test_item['attributes'].get('TEST', '')
        _data_items.append(test_failure)

        server = test_item['machine']
        _data_items.append(server)

        container = test_item['attributes'].get('CONTAINER', '')
        _data_items.append(container)

        tst_r3 = test_item['attributes'].get('TESTR3', '')
        if tst_r3:
            gb_sn = tst_r3.split('|')[0]
            gb_pn = tst_r3.split('|')[1]
        else:
            gb_sn = ''
            gb_pn = ''
        _data_items.append(gb_sn)
        _data_items.append(gb_pn)

        if passfail not in ['P', 'F']:
            continue
        if uuttype.startswith('1783') and not sernum.startswith('SV'):
            continue

        _data_results.append(_data_items)

    # pprint.pprint(_data_results)
    save_to_excel('excel/{}.xlsx'.format(date_now), _data_results)


def save_to_excel(filename, final_datas):
    # 创建一个新的Excel工作簿
    wb = openpyxl.Workbook()

    # 获取默认的工作表Sheet
    sheet = wb.active

    # 向Sheet添加表头
    headers = final_datas[0]
    for i, header in enumerate(headers):
        sheet.cell(row=1, column=i + 1, value=header)

    # 添加表头样式
    header_font = Font(bold=True)
    header_fill = PatternFill(fill_type='solid', start_color='BDD7EE', end_color='BDD7EE')
    header_border = Border(bottom=Side(border_style='thin'))
    for i in range(1, len(headers) + 1):
        sheet.cell(row=1, column=i).font = header_font
        sheet.cell(row=1, column=i).fill = header_fill
        sheet.cell(row=1, column=i).border = header_border

    # 向Sheet添加数据
    data = final_datas[1:]

    for r, row in enumerate(data, start=2):
        for c, cell_value in enumerate(row, start=1):
            sheet.cell(row=r, column=c, value=cell_value)

    # 添加数据行样式
    data_border = Border(bottom=Side(border_style='thin', color='D9D9D9'))
    for r in range(2, len(data) + 2):
        for c in range(1, len(headers) + 1):
            sheet.cell(row=r, column=c).border = data_border

    # 自适应列宽
    for column in sheet.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        sheet.column_dimensions[column[0].column_letter].width = adjusted_width

    # 保存Excel文件
    wb.save(filename)


if __name__ == '__main__':
    save_test_record_to_excel(read_last_history())
