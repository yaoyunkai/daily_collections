"""


created at 2025/1/9
"""


class Queue:
    def __init__(self):
        self.__data = []

    def enqueue(self, item):
        self.__data.insert(0, item)

    def dequeue(self):
        return self.__data.pop()

    def is_empty(self):
        return len(self.__data) == 0

    def size(self):
        return len(self.__data)

    def __len__(self):
        return len(self.__data)
