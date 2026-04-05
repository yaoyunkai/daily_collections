"""
单例模式


"""

import logging
import sys
import threading

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d [%(threadName)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",  # 使用 T 分隔日期和时间
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


class Singleton:
    __instance = None
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        # print(f"__new__ {args}, {kwargs}")
        if cls.__instance is None:
            with cls.__lock:
                if cls.__instance is None:
                    cls.__instance = super().__new__(cls)

        return cls.__instance


class SingletonMeta(type):
    __instances = {}
    __lock = threading.Lock()

    # cls 是传入的cls, 比如 Singleton2
    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            with cls.__lock:
                if cls not in cls.__instances:
                    cls.__instances[cls] = super().__call__(*args, **kwargs)

        return cls.__instances[cls]


class Singleton2(metaclass=SingletonMeta):
    def __init__(self, value=None):
        self.value = value


def run_with_singleton():

    def create_singleton(thread_id: int):
        instance = Singleton()
        logger.info("线程 %d 获取实例 ID: %d", thread_id, id(instance))

    if __name__ == "__main__":
        threads = []
        for i in range(10):  # 模拟 10 个并发线程
            t = threading.Thread(target=create_singleton, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        logger.info("所有线程已完成。多线程单例模式测试通过。")


if __name__ == "__main__":
    # obj = Singleton(1234, abc=12)
    run_with_singleton()
