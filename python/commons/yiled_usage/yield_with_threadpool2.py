"""

fut = submit

fut.result()
fut.add_done_callback()



Created at 2023/4/3
"""
import logging
import time
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(format='%(asctime)s - %(threadName)s: %(message)s',
                    level=logging.DEBUG, datefmt='%H:%M:%S', )

logger = logging.getLogger(__name__)


class Task:

    def __init__(self, gen):
        self._gen = gen

    def step(self, value=None, exc=None):
        try:
            if exc:
                fut = self._gen.throw(exc)
            else:
                fut = self._gen.send(value)
            fut.add_done_callback(self._wakeup)
        except StopIteration as e:
            pass

    def _wakeup(self, fut):
        try:
            result = fut.result()
            self.step(result, None)
        except Exception as exc:
            self.step(None, exc)


if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=8)


    def func(x, y):
        time.sleep(1)
        return x + y


    # def do_func(x, y):
    #     # this is a generator
    #     logger.info('start the do_func ....')
    #
    #     # Future
    #     result = yield pool.submit(func, x, y)
    #     logger.info('Got: %s', result)


    def do_many(n):
        logger.info('start the do_func ....')
        while n > 0:
            # result = yield pool.submit(func, n, n)
            result = yield pool.submit(func, n, n)
            logger.info('Got: %s', result)
            n -= 1


    # t = Task(do_func(2, 3))  # 这里不会run do_func
    # t.step()

    t = Task(do_many(10))
    t.step()
