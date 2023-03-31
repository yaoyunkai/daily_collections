"""Download flags of top 20 countries by population

ThreadPoolExecutor version

Future
    done
    add_done_callback
    result

Executor
    map
    submit
    as_completed



"""
# BEGIN FLAGS_THREADPOOL
import os
import sys
import time
from concurrent import futures  # <1>

import requests

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()

BASE_URL = 'https://www.fluentpython.com/data/flags/'

DEST_DIR = 'downloads/'

MAX_WORKERS = 20  # <2>


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content


def show(text):
    print(text, end=' ')
    sys.stdout.flush()


def download_one(cc):  # <3>
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))  # <4>
    with futures.ThreadPoolExecutor(workers) as executor:  # <5>
        res = executor.map(download_one, sorted(cc_list))  # <6>

    return len(list(res))  # <7>


def main():  # <10>
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main()
# END FLAGS_THREADPOOL
