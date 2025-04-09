"""

有序队列，基于链表实现

created at 2025/4/9
"""


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class OrderedList:

    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def add(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def length(self):
        cur = self.head
        cnt = 0
        while cur is not None:
            cnt += 1
            cur = cur.next

        return cnt
