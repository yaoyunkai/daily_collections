"""
分析数据

yield type & data_type
    First Pass Yield
    Test  Yield
    Board Yield

view type:
    none
    month
    week

test_result:
    default is P F , optional is A : adt sampling, S start record


"""
import datetime
import re

DATE_PATTERN = re.compile(r'^(\d{4})-(\d{2})-(\d{2})$')
PARAM_SEPARATOR = ','


def _check_date(date_string):
    result = DATE_PATTERN.search(date_string)
    if not result:
        return False
    try:
        datetime.date(*[int(i) for i in result.groups()])
        return True
    except Exception:
        return False


def _check_pattern_match(_string):
    """
    Mysql Pattern Match:
    use _ to match any single character and
        % to match an arbitrary number of characters (including zero characters)

    :return:
    """
    if '%' in _string or '_' in _string:
        return True
    return False


def _deal_with_common_param(common_param):
    """
    common_params can be list or str

    PCBST
    PCBST,PCB2C
    ['PCBFT', 'PCBPM']
    ['PCBFT', 'PCBPM, PCBFT']
    PCB%,ASSY

    return [(value, pattern_flag: True or False), ]

    :param common_param:
    :return:
    """
    _result = []

    if not common_param:
        return _result

    if type(common_param) not in [str, list]:
        raise TypeError('query params only support str and list')

    if type(common_param) is str:
        if PARAM_SEPARATOR in common_param:
            common_param = common_param.split(PARAM_SEPARATOR)
        else:
            common_param = [common_param, ]

    for param in common_param:
        if type(param) is not str:
            raise TypeError('list element must be string')

        # for check list element still have separator
        if PARAM_SEPARATOR in param:
            param = param.split(PARAM_SEPARATOR)
        else:
            param = [param, ]
        for item in param:
            if item:
                _result.append(
                    (item, _check_pattern_match(item))
                )

    return _result


def _deal_with_params(params_dict: dict, yield_or_search=True):
    """
    for sernum uuttype area and test_server we can support pattern match

    from_date must less to_date


    :param params_dict:
    :param yield_or_search: if True for check yield else for check search
    :return:
    """
    common_params_spec = ['sernum', 'uuttype', 'area', 'test_server']
    date_params_spec = ['from_date', 'to_date']
    yield_params_spec = ['yield_type', 'view_type']
    search_params_spec = ['data_type', 'test_result']

    _result_dict = {}

    for common_param in common_params_spec:
        _param = params_dict.get(common_param)
        if not _param:
            continue
        _result_dict[common_param] = _deal_with_common_param(_param)
    if not _result_dict:
        raise ValueError('must select one Common Params: {}'.format(common_params_spec))


def get_yield(sernum='', uuttype='', area='', test_server='',
              from_date='', to_date='', yield_type='', view_type=''):
    print(locals())


def search_test_record(sernum='', uuttype='', area='', test_server='',
                       from_date='', to_date='', data_type='', test_result=''):
    print(locals())


if __name__ == '__main__':
    print(_deal_with_common_param('PCBST'))
    print(_deal_with_common_param(','))
    print(_deal_with_common_param(''))
    print(_deal_with_common_param([]))
    print(_deal_with_common_param(['', ',']))
    print(_deal_with_common_param(['', '', '']))
    print(_deal_with_common_param('PCBST, PCB2C'))
    print(_deal_with_common_param('PCB%'))
    print(_deal_with_common_param('PCB%, ASSY'))
    print(_deal_with_common_param(['PCBST', 'PCBFT']))
    print(_deal_with_common_param(['PCBST', 'PCBFT, PCB%']))
    print(_deal_with_common_param(['PCBST', 'PCBFT, PCBFT']))
    print(_deal_with_common_param(['PCBST', 'PCBFT, PCBFT']))
    # print(_deal_with_common_param([['PCBST', 'PCBFT, PCBFT'], []]))
