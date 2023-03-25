"""
Condition


Created at 2023/2/18
"""

import logging
import threading
import time

logging.basicConfig(format='%(asctime)s - %(threadName)s: %(message)s',
                    level=logging.DEBUG, datefmt='%H:%M:%S')

logger = logging.getLogger(__name__)


class Producer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True

    # 生产者函数
    def run(self):
        global count
        while True:
            if condition.acquire():
                # 当count 小于等于1000 的时候进行生产
                if count > 1000:
                    condition.wait()
                else:
                    count = count + 10
                    msg = ' produce 10, count=' + str(count)
                    logger.debug(msg)
                    # 完成生成后唤醒waiting状态的线程，
                    # 从waiting池中挑选一个线程，通知其调用acquire方法尝试取到锁
                    condition.notify_all()
                condition.release()
                time.sleep(1)


class Consumer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True

    # 消费者函数
    def run(self):
        global count
        while True:
            # 当count 大于等于100的时候进行消费
            if condition.acquire():
                if count < 100:
                    condition.wait()

                else:
                    count = count - 5
                    msg = ' consume 5, count=' + str(count)
                    logger.debug(msg)
                    condition.notify()
                    # 完成生成后唤醒waiting状态的线程，
                    # 从waiting池中挑选一个线程，通知其调用acquire方法尝试取到锁
                condition.release()
                time.sleep(1)


def test():
    for i in range(2):
        p = Producer()
        p.start()
    for i in range(7):
        c = Consumer()
        c.start()

    try:
        while True:
            pass
    except Exception as e:
        logger.error(e)
        logger.debug('main thread ended')


if __name__ == '__main__':
    count = 500
    condition = threading.Condition()
    test()
