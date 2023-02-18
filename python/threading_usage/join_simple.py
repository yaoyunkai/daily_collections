"""
Join


Created at 2023/2/18
"""

import logging
import threading
import time

logging.basicConfig(format='%(asctime)s - %(thread)5d: %(message)s',
                    level=logging.DEBUG, datefmt='%H:%M:%S')

logger = logging.getLogger(__name__)


def do_func():
    logger.debug('do func start')
    time.sleep(3)
    logger.debug('do func end')


if __name__ == '__main__':
    logger.debug('main start')
    arr = []

    # for i in ['A', 'B', "C"]:
    #     thread = threading.Thread(target=do_func, name='thread-{}'.format(i))
    #     thread.start()
    #     arr.append(thread)
    #
    # for i in arr:
    #     i.join()

    for i in ['A', 'B', "C"]:
        thread = threading.Thread(target=do_func, name='thread-{}'.format(i))
        thread.start()
        thread.join()

        arr.append(thread)

    logger.debug('main end')
