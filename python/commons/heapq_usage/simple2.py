"""
heapq

小根堆

堆数据结构最重要的特征是 heap[0] 永远是最小的元素。
并且剩余的元素可以很容易的通过调用 heapq.heappop() 方法得到，
 该方法会先将第一个元素弹出来，然后用下一个最小的元素来取代被弹出元素
 （这种操作时间复杂度仅仅是 O(log N)，N 是堆大小）。

heappush

heappop

heappushpop

heapify: list x 转换为heap inplace

heapreplace

merge: 将多个已排序的输入合并为一个已排序的输出


Created at 2023/3/25
"""

import heapq

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(heapq.nlargest(3, nums))  # Prints [42, 37, 23]
print(heapq.nsmallest(3, nums))  # Prints [-4, 1, 2]

portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'HPQ', 'shares': 35, 'price': 31.75},
    {'name': 'YHOO', 'shares': 45, 'price': 16.35},
    {'name': 'ACME', 'shares': 75, 'price': 115.65}
]
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])
