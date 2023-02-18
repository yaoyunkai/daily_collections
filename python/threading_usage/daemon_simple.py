"""
deamon 线程称为后台，适用于没有持有资源的线程，这样就不需要手动管理这些线程了


Created at 2023/2/18
"""
import logging
import threading
import time

logging.basicConfig(format='%(thread)d: %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)


def do_run():
    count = 0

    # 当在子线程中使用 while True,可以将其设置为 daemon
    while True:
        count += 1
        logger.debug('current count %s', count)
    # logger.debug('never run this')


if __name__ == '__main__':
    logger.debug('---- start main threading ----')
    threading.Thread(target=do_run, daemon=True).start()
    time.sleep(3)
    logger.debug('---- end main threading ----')
