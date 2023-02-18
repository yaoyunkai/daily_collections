"""


Created at 2023/2/18
"""
import logging
import threading
import time
from queue import Queue

logging.basicConfig(format='%(asctime)s - %(threadName)s: %(message)s',
                    level=logging.DEBUG, datefmt='%H:%M:%S')

logger = logging.getLogger(__name__)


class Goods:
    _count = 1
    _lock = threading.RLock()

    def __init__(self, name):
        self.name = name
        with Goods._lock:
            self._id = Goods._count
            Goods._count += 1

    def __str__(self):
        return '<{}-{}>'.format(self.name, self._id)


class ProducerThread(threading.Thread):
    def __init__(self, name, speed, q):
        super().__init__()
        self.daemon = True
        self.name = '{}-P-thread'.format(name)
        self.speed = 1.0 / speed
        self._queue = q

    def run(self):
        while True:
            g = Goods(self.name)
            self._queue.put(g)
            logger.debug('producer a goods: {}'.format(g))
            time.sleep(self.speed)


class ConsumerThread(threading.Thread):
    def __init__(self, name, speed, q):
        super().__init__()
        self.daemon = True
        self.name = '{}-C-thread'.format(name)
        self.speed = 1.0 / speed
        self._queue = q

    def run(self):
        while True:
            goods = self._queue.get()
            logger.debug('consumer a goods: {}'.format(goods))
            time.sleep(self.speed)
            self._queue.task_done()


if __name__ == '__main__':
    queue = Queue()

    t1 = ProducerThread('桃子', speed=5, q=queue)
    t2 = ConsumerThread('Tim', speed=2, q=queue)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
