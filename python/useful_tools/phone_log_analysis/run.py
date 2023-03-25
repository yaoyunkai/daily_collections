"""

log 中包含的信息：
时间
hostname
process_name
pid
log_level_name
message

-----------------------------------
所以redis中的key可以为 logs:<hostname>:<process_name>:<level> -> hash {time: '',  : ''}


Create at 2023/2/19 12:19
"""

import redis

demo_file_path = r'D:\projects\code\python\demo1\demos\logs\20230129_223749_798_iPhone.log'

date_str_dict = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'June': 6,
    'Jul': 7,
    'July': 7,
    'Aug': 8,
    'Sep': 9,
    'Sept': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
}


def get_redis_conn():
    return redis.Redis(host='127.0.0.1', port=6379, db=1)


if __name__ == '__main__':
    # save_log_item('logs:myphone:passd:Notice', '2022-10-19 23:44:13', 'this is a demo message')
    pass
