"""

event 对象最好单次使用，就是说，你创建一个 event 对象，让某个线程等待这个对象，
一旦这个对象被设置为真，你就应该丢弃它。
尽管可以通过 clear() 方法来重置 event 对象，但是很难确保安全地清理 event 对象并对它重新赋值。
很可能会发生错过事件、死锁或者其他问题（特别是，你无法保证重置 event 对象的代码会在线程再次等待这个 event 对象之前执行）。


Created at 2023/3/28
"""

import logging
import time
from threading import Thread, Event

logging.basicConfig(format='%(asctime)s - %(threadName)s: %(message)s',
                    level=logging.DEBUG, datefmt='%H:%M:%S')

logger = logging.getLogger(__name__)


# Code to execute in an independent thread
def countdown(n, event):
    logger.info('countdown starting')
    while n > 0:
        logger.info('T-minus: %s', n)
        n -= 1
        time.sleep(2)
    event.set()


if __name__ == '__main__':
    # Create the event object that will be used to signal startup
    started_evt = Event()

    # Launch the thread and pass the startup event
    logger.info('Launching countdown')
    t = Thread(target=countdown, args=(10, started_evt))
    t.start()

    # Wait for the thread to start
    started_evt.wait()
    logger.info('countdown is ending')
