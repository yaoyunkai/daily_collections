"""
Compute yield use python

uut_type  board_qty ete area1 area2 area3

_Total:   board_qty  ete area1 area2 area3

FP: include sampling data

test: not include sampling data


"""
import json
import pprint
from collections import Counter

ETE = 'ETE'


def get_test_record():
    fp = open(r'C:\code\libyao_projects\demos\test_record\demo.json', mode='r')
    return json.load(fp)


def compute_first_pass_yield():
    # must be ordered test records
    test_records = get_test_record()

    _yield_dict = {}  # group by uut_type, area / ETE not group by area
    _zzz_yield_dict = {}  # group by area / ETE not group by area

    for item in test_records:
        item_record_time = item['record_time']
        item_area = item['area']
        item_uuttype = item['uuttype']
        item_sernum = item['sernum']
        item_test_result = item['test_result']

        if item_uuttype not in _yield_dict:
            _yield_dict[item_uuttype] = {}
            _yield_dict[item_uuttype][ETE] = {}  # sernum: pass_fail

        if item_area not in _yield_dict[item_uuttype]:
            _yield_dict[item_uuttype][item_area] = {}  # sernum: pass_fail

        if item_test_result not in ['P', 'F']:
            continue

        for area, d in _yield_dict[item_uuttype].items():
            if area == ETE:
                continue
            if area == item_area:
                if item_sernum not in d:
                    d[item_sernum] = item_test_result

                    if item_sernum not in _yield_dict[item_uuttype][ETE]:
                        _yield_dict[item_uuttype][ETE][item_sernum] = item_test_result
                    else:
                        if item_test_result == 'F':
                            _yield_dict[item_uuttype][ETE][item_sernum] = item_test_result

    # pprint.pprint(_yield_dict)
    _new_yield_dict = dict()

    for uuttype, uuttype_data in _yield_dict.items():
        if uuttype not in _new_yield_dict:
            _new_yield_dict[uuttype] = {}

        board_qty = 0
        avg_rate = [0, 0]  # float

        for area, data in uuttype_data.items():
            if area not in _new_yield_dict[uuttype]:
                _new_yield_dict[uuttype][area] = {}

            _counter = Counter(list(data.values()))
            pass_cnt = _counter.get('P', 0)
            fail_cnt = _counter.get('F', 0)
            total_cnt = len(data)

            data = dict(
                pass_cnt=pass_cnt, fail_cnt=fail_cnt, total_cnt=total_cnt, rate=round(pass_cnt / total_cnt, 4) * 100
            )
            _new_yield_dict[uuttype][area] = data
            if area == ETE:
                board_qty = total_cnt
            else:
                avg_rate[0] += pass_cnt
                avg_rate[1] += total_cnt
        avg_rate = round(avg_rate[0] / avg_rate[1], 4) * 100

        _new_yield_dict[uuttype]['board_qty'] = board_qty
        _new_yield_dict[uuttype]['avg_rate'] = avg_rate

    pprint.pprint(_new_yield_dict)


if __name__ == '__main__':
    compute_first_pass_yield()
