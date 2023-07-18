"""


Created at 2023/7/17
"""
import datetime
import json
from collections import defaultdict

from convert_data import save_to_excel


def read_data(test_record_list=None):
    """
    excel headers:
    server, container, fail_count, total_count, failure_items

    """
    if test_record_list:
        test_records = test_record_list
    else:
        data = json.load(open('bst_simple.txt'))
        test_records = data['results']['data']

    _result_dict = {}
    _area_total_failures = {}

    for item in test_records:
        server = item['machine']
        container = item['attributes'].get('CONTAINER', '')
        test_area = item['area']
        pass_fail = item['passfail']
        record_time = item['rectime']
        gb_line = item['attributes'].get('TESTR3', '')
        failure_name = item['attributes'].get('TEST', '')

        if not container:
            continue

        if test_area not in _area_total_failures:
            _area_total_failures[test_area] = defaultdict(int)

        if test_area not in _result_dict:
            _result_dict[test_area] = {}

        if server not in _result_dict[test_area]:
            _result_dict[test_area][server] = {}

        if container not in _result_dict[test_area][server]:
            _result_dict[test_area][server][container] = {}
            _result_dict[test_area][server][container]['fail_count'] = 0
            _result_dict[test_area][server][container]['total_count'] = 0
            _result_dict[test_area][server][container]['failure_items'] = defaultdict(int)

        _result_dict[test_area][server][container]['total_count'] += 1
        if pass_fail in ['F', 'f']:
            _result_dict[test_area][server][container]['fail_count'] += 1
            if failure_name:
                _result_dict[test_area][server][container]['failure_items'][failure_name] += 1

                # if test_area in ['PCBST', 'PCBFT', 'PCBPM']:
                #     if failure_name.startswith('GO TO BOOT LOADER'):
                #         _area_total_failures[test_area]['GO TO BOOT LOADER'] += 1
                #     elif failure_name.startswith('GO TO DIAG'):
                #         _area_total_failures[test_area]['GO TO DIAG'] += 1
                #     elif failure_name.startswith('SYSTEM INITIALIZE'):
                #         _area_total_failures[test_area]['SYSTEM INITIALIZE'] += 1
                #     elif failure_name.startswith('TRAFFIC SPEED'):
                #         _area_total_failures[test_area]['TRAFFIC TEST'] += 1
                # else:
                _area_total_failures[test_area][failure_name] += 1

    # pprint.pprint(_result_dict)
    # pprint.pprint(_area_total_failures)

    get_excel_data_list(_result_dict, _area_total_failures)


def get_failure_top_list(dict_data, test_area, top=12):
    sorted_keys = sorted(dict_data[test_area], key=dict_data[test_area].get, reverse=True)[:top]
    return sorted_keys


def get_excel_data_list(result_dict, area_total_failures):
    # final_excel_list = []
    # excel_headers = ['server', 'container', 'fail_count', 'total_count']

    date_now = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

    for area, one_data in result_dict.items():
        final_excel_list = []

        # 通过控制 failure_list 可以控制 failure single item
        failure_list = get_failure_top_list(area_total_failures, area)
        excel_headers = ['server', 'container', 'fail_count', 'total_count']
        excel_headers.extend(failure_list)

        final_excel_list.append(excel_headers)

        for server, two_data in one_data.items():
            for container, final_data in two_data.items():
                one_data = [server, container, final_data['fail_count'], final_data['total_count']]

                for failure_item in failure_list:
                    one_data.append(final_data['failure_items'][failure_item])
                # print(one_data)
                final_excel_list.append(one_data)

        # pprint.pprint(final_excel_list)

        save_to_excel('excel2/{}_{}.xlsx'.format(date_now, area), final_excel_list)


if __name__ == '__main__':
    read_data()
