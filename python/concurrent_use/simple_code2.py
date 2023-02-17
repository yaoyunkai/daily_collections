"""


Create at 2023/2/17 22:38
"""

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(format='%(thread)d: %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)


def demo_func():
    logger.debug('start demo_func')
    time.sleep(3)
    logger.debug('end demo_func')


def run_in_executor():
    executor = ThreadPoolExecutor(max_workers=3)
    thread_pool = []
    for idx in range(10):
        future = executor.submit(demo_func)
        thread_pool.append(future)

    for f in as_completed(thread_pool):
        try:
            f.result()
        except Exception as e:
            executor.shutdown(wait=False)
            raise e


if __name__ == '__main__':
    run_in_executor()
