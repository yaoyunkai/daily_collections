"""
分析数据

from request(django) user input params is be str or [str, ...]

yield type & data_type
    First Pass Yield : fp
    Test  Yield      : test
    Board Yield      : board

view type:
    none
    month
    week

test_result:
    default is P F , optional is A : adt sampling, S start record


"""
import datetime
import pprint
import re

TEST_RESULT_PATTERN = re.compile(r'^[PSFA](,[PSFA])*$', )
DATE_PATTERN = re.compile(r'^(\d{4})-(\d{1,2})-(\d{1,2})$')

PARAM_SEPARATOR = ','


def check_date_string(date_string: str):
    result = DATE_PATTERN.search(date_string)
    if not result:
        return False
    # noinspection PyBroadException
    try:
        datetime.date(*[int(i) for i in result.groups()])
        return True
    except Exception:
        return False


def get_date_from_string(date_string: str):
    result = DATE_PATTERN.search(date_string)
    if not result:
        return None
    # noinspection PyBroadException
    try:
        return datetime.date(*[int(i) for i in result.groups()])
    except Exception:
        return None


def _deal_with_common_param(common_param: str):
    """
    common_params is str
    return [(value, pattern_flag: True or False), ...]

    PCB%%  这种写法会不会对SQL有什么影响

    :param common_param:
    :return:
    """
    _result = []

    if not common_param:
        return _result

    if PARAM_SEPARATOR in common_param:
        common_param = common_param.split(',')
    else:
        common_param = [common_param, ]

    for item in common_param:
        if not item:
            continue

        item = item.strip()
        if not item.replace('%', '').replace('_', ''):
            continue

        if '%' in item or '_' in item:
            _result.append((item, True))
        else:
            _result.append((item, False))

    return _result


def _deal_with_params(params_dict: dict, yield_or_search=True):
    """
    for sernum uuttype area and test_server we can support pattern match

    from_date must less to_date

    common_params_spec = ['sernum', 'uuttype', 'area', 'test_server']
    # date_params_spec = ['from_date', 'to_date']
    # yield_params_spec = ['yield_type', 'view_type']
    # search_params_spec = ['data_type', 'test_result']

    :param params_dict:
    :param yield_or_search: if True for check yield else for check search
    :return:
    """
    common_params_spec = ['sernum', 'uuttype', 'area', 'test_server']
    _final_result = {}

    # check common params
    for param_name in common_params_spec:
        param = params_dict.get(param_name)
        if not param:
            continue
        _formatted_param = _deal_with_common_param(param)
        if not _formatted_param:
            continue
        _final_result[param_name] = _formatted_param
    if not _final_result:
        raise ValueError('must input at least one common params: {}'.format(common_params_spec))

    # check from_date and to_date
    from_date = get_date_from_string(params_dict.get('from_date', ''))
    to_date = get_date_from_string(params_dict.get('to_date', ''))
    if not from_date or not to_date:
        raise ValueError('must input from_date and to_date')
    if from_date > to_date:
        raise ValueError('from_date must less than to_date')
    _final_result['from_date'] = from_date
    _final_result['to_date'] = to_date

    # check special params
    if yield_or_search:
        yield_type = params_dict.get('yield_type', 'fp')
        view_type = params_dict.get('view_type', 'none')
        if yield_type not in ['fp', 'test', 'board']:
            raise ValueError("yield_type must be 'fp', 'test', 'board'")
        if view_type not in ['none', 'month', 'week']:
            raise ValueError("view_type must be 'none', 'month', 'week'")
        _final_result['yield_type'] = yield_type
        _final_result['view_type'] = view_type

    else:
        data_type = params_dict.get('data_type', 'test')
        test_result = params_dict.get('test_result', 'P,F')
        if data_type not in ["test", "fp", "board"]:
            raise ValueError('data_type must be "test", "fp", "board"')
        if not TEST_RESULT_PATTERN.match(test_result):
            raise ValueError('test_result must be P,F,S,A')
        _final_result['data_type'] = data_type
        _final_result['test_result'] = test_result

    return _final_result


def get_yield(
        sernum='', uuttype='', area='', test_server='',
        from_date='', to_date='',
        yield_type='', view_type=''):
    _result = _deal_with_params(locals(), yield_or_search=True)
    pprint.pprint(_result)


def search_test_record(
        sernum='', uuttype='', area='', test_server='',
        from_date='', to_date='',
        data_type='', test_result=''):
    pass


if __name__ == '__main__':
    get_yield(uuttype='IE%', from_date='2020-1-1', to_date='2022-2-1',
              yield_type='fp', view_type='none')
