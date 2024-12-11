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

    def step(self, value=None):
        logger.info('start Task step')
        try:

            # fut 是 yield后面的片段: Future
            fut = self._gen.send(value)
            logger.info('gen called after send, fut: {}'.format(fut))
            fut.add_done_callback(self._wakeup)
        except StopIteration as e:
            logger.info('Get error: %s', e)
            # 在 第二次call step时,会在 fut = 报错。
            pass

    def _wakeup(self, fut):
        # fut 会被done_callback传入, 也就是pool
        logger.info('start done callback now...')
        result = fut.result()
        self.step(result)  # 再次调用send(result) 把结果传给 do_func


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
