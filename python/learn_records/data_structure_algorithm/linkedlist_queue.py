"""


created at 2025/1/9
"""


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def __len__(self):
        return self._size

    def enqueue(self, item):
        new_node = Node(item)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        value = self.head.value
        self.head = self.head.next
        self._size -= 1
        if self.is_empty():
            self.tail = None
        return value


def hot_potato(name_list, num):
    queue = Queue()

    for name in name_list:
        queue.enqueue(name)

    while queue.size() > 1:
        for i in range(num):
            queue.enqueue(queue.dequeue())

        queue.dequeue()

    return queue.dequeue()


if __name__ == '__main__':
    rrr = hot_potato(["Bill", "David", "Susan", "Jane", "Kent", "Brad"], 7)
    print(rrr)
