"""

created at 2025/5/2
"""
import os.path
import time

import requests

base_dir = 'my_data'


def save_to_file(content, filename):
    try:
        with open(filename, mode='w', encoding='utf8') as f:
            f.write(content)
    except Exception as e:
        print(e)


def get_total_1000(user_id=None):
    url = 'http://127.0.0.1:11451//v1/GetMatchHistory?filterQueueId=0&filterChampionId=0&begIndex={}&endIndex={}'

    if user_id:
        url += f'&puuid={user_id}'

    for i in range(100):
        start = i * 10
        end = (i + 1) * 10 - 1
        # print(f'start: {start}, end: {end}')
        real_url = url.format(start, end)
        print(real_url)
        filename = 'demo{}.json'.format(i)

        resp = requests.get(real_url)
        save_to_file(resp.content.decode('utf8'), os.path.join(base_dir, filename))

        time.sleep(1.5)


if __name__ == '__main__':
    # get_total_1000()
    pass
