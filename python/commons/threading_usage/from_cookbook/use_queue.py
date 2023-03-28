"""

Queue 对象已经包含了必要的锁，所以你可以通过它在多个线程间多安全地共享数据。
当使用队列时，协调生产者和消费者的关闭问题可能会有一些麻烦。
一个通用的解决方法是在队列中放置一个特殊的值，当消费者读到这个值的时候，终止执行。


q.qsize() ， q.full() ， q.empty() 等实用方法可以获取一个队列的当前大小和状态。
但要注意，这些方法都不是线程安全的。


Created at 2023/3/28
"""
import logging
import time
from queue import Queue
from threading import Thread

_sentinel = object()
logging.basicConfig(format='%(asctime)s - %(threadName)s: %(message)s',
                    level=logging.DEBUG, datefmt='%H:%M:%S', )
logger = logging.getLogger(__name__)


# A thread that produces data
def producer(out_q):
    n = 10
    while n > 0:
        # Produce some data
        out_q.put(n)
        logger.info('producer put data: %s', n)

        time.sleep(2)
        n -= 1

    # Put the sentinel on the queue to indicate completion
    out_q.put(_sentinel)
    logger.info('producer put data: %s', 'final')


# A thread that consumes data
def consumer(in_q):
    while True:
        # Get some data
        data = in_q.get()

        # Check for termination
        if data is _sentinel:
            # 消费者在读到这个特殊值之后立即又把它放回到队列中，将之传递下去。
            in_q.put(_sentinel)
            break

        # Process the data
        logger.info('Got: %s', data)
    logger.info('Consumer shutting down')


if __name__ == '__main__':
    q = Queue()
    t1 = Thread(target=consumer, args=(q,))
    t2 = Thread(target=producer, args=(q,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
