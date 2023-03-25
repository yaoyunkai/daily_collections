"""


Created at 2023/2/18
"""
import logging
import threading
import time

logging.basicConfig(format='%(asctime)s - %(threadName)s: %(message)s',
                    level=logging.DEBUG, datefmt='%H:%M:%S')

logger = logging.getLogger(__name__)


def func():
    # 等待事件，进入等待阻塞状态
    logger.debug('wait for event...')
    event.wait()
    # 收到事件后进入运行状态
    logger.debug('recv event.')


if __name__ == '__main__':
    event = threading.Event()

    t1 = threading.Thread(target=func)
    t2 = threading.Thread(target=func)
    t1.start()
    t2.start()

    time.sleep(2)

    # 发送事件通知
    logger.debug('MainThread set event.')
    event.set()
