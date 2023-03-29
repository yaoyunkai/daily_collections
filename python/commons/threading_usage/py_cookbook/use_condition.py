"""


Created at 2023/3/28
"""

import logging
import threading
import time

logging.basicConfig(format='%(asctime)s - %(threadName)s: %(message)s',
                    level=logging.DEBUG, datefmt='%H:%M:%S', )
logger = logging.getLogger(__name__)


class PeriodicTimer:
    def __init__(self, interval):
        self._interval = interval
        self._flag = 0
        self._cv = threading.Condition()

    def start(self):
        t = threading.Thread(target=self.run)
        t.daemon = True

        t.start()

    def run(self):
        """
        Run the timer and notify waiting threads after each interval
        """
        while True:
            time.sleep(self._interval)
            with self._cv:
                # flag 会周期性的 0 1 变化
                self._flag ^= 1
                # logger.info('the flag is: %s', self._flag)
                self._cv.notify_all()

    def wait_for_tick(self):
        """
        Wait for the next tick of the timer
        """
        with self._cv:
            last_flag = self._flag
            logger.info('============== last flag: %s', self._flag)
            while last_flag == self._flag:
                logger.info('*********************** wait condition start')
                self._cv.wait()
                logger.info('*********************** wait condition end')


# Two threads that synchronize on the timer
def countdown(nticks):
    while nticks > 0:
        logger.info('>>>>>>>>>>>>>> before wait for tick')
        ptimer.wait_for_tick()
        logger.info('<<<<<<<<<<<<<<  after wait for tick')

        logger.info('T-minus: %s', nticks)
        nticks -= 1


def countup(last):
    n = 0
    while n < last:
        ptimer.wait_for_tick()
        logger.info('Counting: %s', n)
        n += 1


if __name__ == '__main__':
    # Example use of the timer
    ptimer = PeriodicTimer(2)
    ptimer.start()

    threading.Thread(target=countdown, args=(10,)).start()
    # threading.Thread(target=countup, args=(5,)).start()
