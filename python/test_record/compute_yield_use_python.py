"""
Compute yield use python

uut_type  board_qty ete area1 area2 area3

_Total:   board_qty  ete area1 area2 area3



"""
import json
import pprint


def get_test_record():
    fp = open('demo.json', mode='r')
    return json.load(fp)


def compute_yield():
    # ordered test record
    test_records = get_test_record()

    _yield_dict = {}
    _zzz_yield_dict = {}

    for item in test_records:
        _record_time = item['record_time']
        _area = item['area']
        _uuttype = item['uuttype']
        _sernum = item['sernum']
        _test_result = item['test_result']

        if _uuttype not in _yield_dict:
            _yield_dict[_uuttype] = {}
            _yield_dict[_uuttype]['ETE'] = {'P': set(), 'F': set(), 'T': set()}

        if _area not in _yield_dict[_uuttype]:
            _yield_dict[_uuttype][_area] = {'P': [], 'F': [], 'T': []}

        if _test_result not in ['P', 'F']:
            continue

        for dict_area, dict_area_data in _yield_dict[_uuttype].items():
            if dict_area == 'ETE':
                continue
            if dict_area == _area:
                if _sernum not in dict_area_data['T']:
                    dict_area_data['T'].append(_sernum)
                    _yield_dict[_uuttype]['ETE']['T'].add(_sernum)
                    if _test_result == 'F':
                        dict_area_data['F'].append(_sernum)
                    else:
                        dict_area_data['P'].append(_sernum)

    pprint.pprint(_yield_dict)


if __name__ == '__main__':
    compute_yield()
