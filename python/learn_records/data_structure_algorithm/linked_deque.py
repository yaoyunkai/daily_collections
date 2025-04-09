"""

基于链表的双端队列

实现线程安全。Lock与RLock



created at 2025/4/9
"""

_null = object()


class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

    def __str__(self):
        return f'Node<{self.value}>'


class Deque:
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def add_front(self, item):
        new_node = Node(item)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            new_node.next = self.front
            self.front.prev = new_node
            self.front = new_node
        self._size += 1

    def add_rear(self, item):
        new_node = Node(item)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            new_node.prev = self.rear
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1

    def remove_front(self):
        if self.is_empty():
            raise IndexError('empty Deque')
        value = self.front.value
        if self.front == self.rear:
            self.front = self.rear = None
        else:
            self.front = self.front.next
            self.front.prev = None
        self._size -= 1
        return value

    def remove_rear(self):
        if self.is_empty():
            raise IndexError('empty Deque')
        value = self.rear.value
        if self.rear == self.front:
            self.rear = self.front = None
        else:
            self.rear = self.rear.prev
            self.rear.next = None

        self._size -= 1
        return value


def pal_checker(value: str):
    """
    回文检测

    """

    queue = Deque()
    for char in value:
        queue.add_rear(char)

    equal = True

    while queue.size() > 1 and equal:
        first = queue.remove_front()
        last = queue.remove_rear()

        if first != last:
            equal = False

    return equal


if __name__ == '__main__':
    q = Deque()

    q.add_front(1)
    q.add_rear(2)
    q.add_front(4)
    q.add_rear(6)

    ret = pal_checker('ssseddweraf')
    print(ret)
    ret = pal_checker('asdrdsa')
    print(ret)
