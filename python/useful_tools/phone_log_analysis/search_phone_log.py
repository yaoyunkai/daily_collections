r"""
Created at 2023/7/29

把日志文件分解为单个的item

log header: Jul 29 10:05:01 qazwsx locationd[70] <Notice>:

一行的log可能会出现断行的情况
log header 也有可能断行，那怎么判断 ?????
一个log的内容也可能不在一行里面

function name with log tags --> monitor


"""
import re
from typing import Callable, Union

import numpy

# https://regex101.com/r/7BcnA2/1
LOG_HEADER_PATTERN = re.compile(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec})\s+\d{1,2} '
                                r'\d{1,2}:\d{1,2}:\d{1,2}) (\w+) (.*?)\[\d+] <([A-Z][a-zA-Z]+)>: ')


def get_month(value: str) -> int:
    _tmp = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    return _tmp.index(value) + 1


def read_log_content(filepath: str):
    """
    get log all content from somewhere
    
    :param filepath: 
    :return: 
    """
    fp = open(filepath, mode='r')
    content = fp.read()
    fp.close()
    return content


def deal_with_log(contents: str, log_header: Union[str, re.Pattern, re.Pattern[str]], action_call: Callable):
    """
    提取log item, 分解为单个的log，
    
    所以 log_header 和 callback 应该匹配
    
    :param action_call: callback方法只支持位置参数
    :param contents: 
    :param log_header: 
    :return: 
    """
    log_line_list = contents.splitlines()
    log_line_list_len = len(log_line_list)

    idx = 0

    while idx < log_line_list_len:
        # read option
        line = log_line_list[idx]

        if log_header.search(line):
            log_item = line

            end_idx = idx + 1
            while end_idx < log_line_list_len:
                inner_line = log_line_list[end_idx]

                if log_header.search(inner_line):
                    # 如果是log header, 说明上一个log item已经结束
                    break
                else:
                    # 换行符被去掉了
                    log_item += inner_line
                    idx += 1

                end_idx += 1

            duplicated_log_item = log_header.findall(log_item)
            if len(duplicated_log_item) > 1:

                item_length = len(duplicated_log_item[0])
                # 填补一个log message的位置
                item_length += 1

                result = re.split(log_header, log_item, )[1:]  # 去掉开头的空item
                if len(result) % item_length == 0:
                    result = numpy.reshape(result, (len(duplicated_log_item), item_length))
                    for _log_item in result:
                        action_call(*_log_item)
            else:
                log_message = re.sub(log_header, '', log_item)
                action_call(*duplicated_log_item[0], log_message)

        idx += 1


# conn = MySQLdb.connect(
#     host='localhost',
#     port=3306,
#     db='python_demo1',
#     user='root',
#     password='password',
# )
# 
# _sql = """
# insert into phone_logs (record_time, hostname, process_name, log_level, log_message)
# values (%s, %s, %s, %s, %s)
# """
# 
# results = []


def action_for_iphone_log_item(date_str, hostname, process_name, log_level, log_message):
    """
    
    :param date_str: 
    :param hostname: 
    :param process_name: 
    :param log_level: 
    :param log_message: 
    :return: 
    """
    # print(process_name, log_message)

    # month, day, hours = date_str.split()
    # month = get_month(month)
    # 
    # date_str = '{}-{}-{} {}'.format(2023, month, day, hours)
    # 
    # results.append([date_str, hostname, process_name, log_level, log_message])


if __name__ == '__main__':
    # print(read_log_content('20230729_100506_469_qazwsx.log'))
    deal_with_log(read_log_content('20230729_100506_469_qazwsx.log'), LOG_HEADER_PATTERN, action_for_iphone_log_item)
