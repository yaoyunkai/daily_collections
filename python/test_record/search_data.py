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

---------------------------------------------------------------------------
Test Yield: 这个最简单，不用做任何处理，按时间段来取数据即可

F, P, T : test_result 为 F P & FP


first pass yield: 获取数据：时间段，该时间段内，某个工站的某个SN的第一笔测试记录。
F:  记录中每个SN 只要有Fail的 SN数量
P:  记录中每个SN的所有工站都是PASS的 SN数量
T:  记录中所有不重复的SN的数量

board yield: 该时间段内，某个工站的某个SN的最后一笔测试状态


"""
import datetime
import pprint
import re

from insert_data import get_mysql_conn

TEST_RESULT_PATTERN = re.compile(r'^[PSFA](,[PSFA])*$', )
DATE_PATTERN = re.compile(r'^(\d{4})-(\d{1,2})-(\d{1,2})$')

PARAM_SEPARATOR = ','
COMMON_PARAMS_SPEC = ['sernum', 'uuttype', 'area', 'test_server']


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
    _final_result = {}

    # check common params
    for param_name in COMMON_PARAMS_SPEC:
        param = params_dict.get(param_name)
        if not param:
            continue
        _formatted_param = _deal_with_common_param(param)
        if not _formatted_param:
            continue
        _final_result[param_name] = _formatted_param
    if not _final_result:
        raise ValueError('must input at least one common params: {}'.format(COMMON_PARAMS_SPEC))

    # check from_date and to_date
    from_date = get_date_from_string(params_dict.get('from_date', ''))
    to_date = get_date_from_string(params_dict.get('to_date', ''))
    if not from_date or not to_date:
        raise ValueError('must input from_date and to_date')
    if from_date > to_date:
        raise ValueError('from_date must less than to_date')
    _final_result['from_date'] = datetime.datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0)
    _final_result['to_date'] = datetime.datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59)

    # check special params
    if yield_or_search:
        yield_type = params_dict.get('yield_type') or 'fp'
        view_type = params_dict.get('view_type') or 'none'
        if yield_type not in ['fp', 'test', 'board']:
            raise ValueError("yield_type must be 'fp', 'test', 'board'")
        if view_type not in ['none', 'month', 'week']:
            raise ValueError("view_type must be 'none', 'month', 'week'")
        _final_result['yield_type'] = yield_type
        _final_result['view_type'] = view_type

    else:
        data_type = params_dict.get('data_type', ) or 'test'
        test_result = params_dict.get('test_result', ) or 'P,F'
        if data_type not in ["test", "fp", "board"]:
            raise ValueError('data_type must be "test", "fp", "board"')
        if not TEST_RESULT_PATTERN.match(test_result):
            raise ValueError('test_result must be P,F,S,A')

        test_result = list(set([i.strip() for i in test_result.split(',')]))

        _final_result['data_type'] = data_type
        _final_result['test_result'] = test_result

    return _final_result


def get_yield(
        sernum='', uuttype='', area='', test_server='',
        from_date='', to_date='',
        yield_type='', view_type=''):
    params = _deal_with_params(locals(), yield_or_search=True)
    pprint.pprint(params)


def search_test_record(
        sernum='', uuttype='', area='', test_server='',
        from_date='', to_date='',
        data_type='', test_result=''):
    params_dict = _deal_with_params(locals(), yield_or_search=False)

    sql_params = []
    base_sql = """
    select record_time, sernum, uuttype, area, test_result, run_time, test_failure, test_server, test_container
    from test_record
    where record_time between %s and %s
    """

    sql_params.append(params_dict['from_date'], )
    sql_params.append(params_dict['to_date'], )

    for param_name in COMMON_PARAMS_SPEC:
        param = params_dict.get(param_name)
        if not param:
            continue
        _tmp_arr = []
        for item in param:
            sql_params.append(item[0])
            _tmp_arr.append(' {} {} %s '.format(param_name, 'LIKE' if item[1] else '='))
        base_sql = base_sql + ' AND ({})'.format('or'.join(_tmp_arr))

    base_sql = base_sql + ' AND test_result in %s order by record_time'
    sql_params.append(params_dict['test_result'])

    print(base_sql)
    print(sql_params)

    mysql_conn = get_mysql_conn()
    cursor = mysql_conn.cursor()
    cursor.execute(base_sql, sql_params)
    test_records = cursor.fetchall()
    for record in test_records:
        print(record)


if __name__ == '__main__':
    # get_yield(uuttype='IE%', from_date='2020-1-1', to_date='2022-2-1', yield_type='fp', view_type='none')
    search_test_record(uuttype='IE-%', area='PCBST,PCB2C', from_date='2021-10-1', to_date='2021-10-1',
                       test_result='P,F', data_type='test')
