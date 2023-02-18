"""
A simple demo for use Lock

Created at 2023/2/18
"""
import logging
import threading

logging.basicConfig(format='%(thread)d: %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)

N = 0


def do_func(val=1, iter_time=500):
    global N
    for _ in range(iter_time):
        lock.acquire()
        N += val
        lock.release()


if __name__ == '__main__':
    lock = threading.Lock()

    threading.Thread(target=do_func, args=(1, 500)).start()
    threading.Thread(target=do_func, args=(-2, 1000)).start()
    threading.Thread(target=do_func, args=(3, 300)).start()

    logger.debug(N)
