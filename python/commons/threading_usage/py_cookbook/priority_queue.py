"""


Created at 2023/3/28
"""
import heapq
import threading
import time


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._count = 0
        self._cv = threading.Condition()

    def put(self, item, priority):
        with self._cv:
            heapq.heappush(self._queue, (-priority, self._count, item))
            self._count += 1
            self._cv.notify()

    def get(self):
        with self._cv:
            while len(self._queue) == 0:
                self._cv.wait()
            return heapq.heappop(self._queue)[-1]


def producer(queue):
    print('Producing items')
    queue.put(None, -100)
    queue.put('C', 5)
    queue.put('A', 15)
    queue.put('B', 10)
    queue.put('D', 0)


def consumer(queue):
    time.sleep(5)
    print('Getting items')
    while True:
        item = queue.get()
        if item is None:
            break
        print('Got:', item)
    print('Consumer done')


if __name__ == '__main__':
    q = PriorityQueue()
    t1 = threading.Thread(target=producer, args=(q,))
    t2 = threading.Thread(target=consumer, args=(q,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
