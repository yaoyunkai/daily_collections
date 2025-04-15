"""

优先级队列

二叉堆有两个常见的变体：最小堆（最小的元素一直在队首）与最大堆（最大的元素一直在队首）。

完全二叉树的另一个有趣之处在于，可以用一个列表来表示它

created at 2025/4/15
"""


class PriorityQueue:
    def __init__(self):
        self._pq = list()
        self._pq.append(None)
        self._n = 0

    def insert(self, item):
        self._pq.append(item)
        self._n += 1
        self._swim(self._n)

    def find_min(self):
        if self.is_empty():
            raise ValueError('empty PQ')
        return self._pq[1]

    def delete_min(self):
        if self.is_empty():
            raise ValueError('empty PQ')

        ret_val = self._pq[1]
        self._pq[1] = self._pq[self._n]
        self._n -= 1
        self._pq.pop()
        self._sink(1)
        return ret_val

    def is_empty(self):
        return self._n == 0

    def size(self):
        return self._n

    def build_heap(self, a_list: list):
        idx = len(a_list) // 2
        self._n = len(a_list)
        self._pq = list()
        self._pq.append(None)
        self._pq.extend(a_list[:])

        while idx > 0:
            self._sink(idx)
            idx -= 1

    def _swim(self, idx):
        while idx > 1:
            if self._pq[idx] < self._pq[idx // 2]:
                self._pq[idx // 2], self._pq[idx] = self._pq[idx], self._pq[idx // 2]
            idx = idx // 2

    def _sink(self, idx):
        while 2 * idx <= self._n:
            j = 2 * idx
            if j < self._n and self._pq[j + 1] < self._pq[j]:
                j += 1
            if not (self._pq[j] < self._pq[idx]):
                break
            self._pq[idx], self._pq[j] = self._pq[j], self._pq[idx]
            idx = j


if __name__ == '__main__':
    pq = PriorityQueue()
    pq.insert(5)
    pq.insert(1)
    pq.insert(4)
    pq.insert(6)
    pq.insert(8)
    pq.insert(2)
    pq.insert(0)
    pq.insert(3)
    pq.insert(7)
    pq.insert(10)
    pq.insert(-5)
    pq.insert(-9)
    pq.insert(13)

    print(pq._pq)
    pq.delete_min()
    print(pq._pq)

    pq2 = PriorityQueue()
    list2 = [5, 1, 4, 6, 8, 2, 0, 3, 7, 10, -5, -9, 13]
    pq2.build_heap(list2)

    print(pq2._pq)
