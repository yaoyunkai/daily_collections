"""
Created at 2023/8/29

MaxPQ


"""

import heapq


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))  # 小顶堆  
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]  # 弹出的是元素，不是元组  


class MaxPQ:

    def __init__(self):
        self.data = [None, ]
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return len(self) == 0

    def _swim(self, k):
        while k > 1 and self.data[k // 2] < self.data[k]:
            self.data[k // 2], self.data[k] = self.data[k], self.data[k // 2]
            k = k // 2

    def _sink(self, k):
        pass

    def insert(self, value):
        self.data.append(value)
        self.size += 1
        self._swim(self.size)

    def del_max(self):
        pass

    def __str__(self):
        return str(self.data[1:])


if __name__ == '__main__':
    pq = MaxPQ()
    pq.insert(5)
    pq.insert(8)
    pq.insert(2)
    pq.insert(9)

    print(pq)
