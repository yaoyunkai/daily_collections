"""
id_generator.py


created at 2026-04-25
"""

import multiprocessing
import threading


class MultiprocessIdGenerator:
    """多进程安全的自增 ID 生成器"""

    def __init__(self, start: int = 1):
        # 'i' 表示有符号整数，可根据需要换成 'I'(无符号)等
        self._counter = multiprocessing.Value("i", start)
        self._lock = multiprocessing.Lock()

    def next_id(self) -> int:
        with self._lock:
            current = self._counter.value
            self._counter.value += 1
            return current


if __name__ == "__main__":
    gen = MultiprocessIdGenerator(start=1000)  # 从 1000 开始

    # 在多线程中安全使用
    def worker():
        for _ in range(5):
            print(threading.current_thread().name, gen.next_id())

    threads = [threading.Thread(target=worker) for _ in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
