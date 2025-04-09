"""

有序队列，基于链表实现

created at 2025/4/9
"""


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class ComparableNode(Node):
    def compare(self, other: 'ComparableNode'):
        raise NotImplemented


class UnorderedList:
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

    def __len__(self):
        return self.length()

    def search(self, item):
        cur = self.head
        found = False

        while cur is not None and not found:
            if cur.value == item:
                found = True
            else:
                cur = cur.next
        return found

    def remove(self, item):
        cur = self.head
        prev = None
        found = False

        while cur is not None and not found:
            if cur.value == item:
                found = True
            else:
                prev = cur
                cur = cur.next

        if not found:
            # nothing to do
            raise ValueError('value not found')

        if prev is None:
            self.head = cur.next
        else:
            prev.next = cur.next

    def __str__(self):
        """将链表转换为字符串表示"""
        elements = []
        current = self.head
        while current is not None:
            elements.append(str(current.data))
            current = current.next
        return '[' + ', '.join(elements) + ']'


class OrderedList:

    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def length(self):
        cur = self.head
        cnt = 0
        while cur is not None:
            cnt += 1
            cur = cur.next

        return cnt

    def __len__(self):
        return self.length()

    def add(self, item):
        cur = self.head
        prev = None
        stop = False

        while cur is not None and not stop:
            if cur.value > item:
                stop = True

            else:
                prev = cur
                cur = cur.next

        new_node = Node(item)
        if prev is None:
            new_node.next = self.head
            self.head = new_node
        else:
            new_node.next = cur
            prev.next = new_node

    def search(self, item):
        """
        在无序列表中搜索时，需要逐个遍历节点，直到找到目标节点或者没有节点可以访问。
        这个方法同样适用于有序列表，但前提是列表包含目标元素。
        如果目标元素不在列表中，可以利用元素有序排列这一特性尽早终止搜索。

        """
        cur = self.head

        found = False
        stop = False

        while cur is not None and not found and not stop:
            if cur.value == item:
                found = True
            else:
                if cur.value > item:
                    stop = True
                else:
                    cur = cur.next

        return found

    def remove(self, item):
        cur = self.head
        prev = None
        found = False

        while cur is not None and not found:
            if cur.value == item:
                found = True
            else:
                prev = cur
                cur = cur.next

        if not found:
            # nothing to do
            raise ValueError('value not found')

        if prev is None:
            self.head = cur.next
        else:
            prev.next = cur.next

    def __str__(self):
        """将链表转换为字符串表示"""
        elements = []
        current = self.head
        while current is not None:
            elements.append(str(current.value))
            current = current.next
        return '[' + ', '.join(elements) + ']'


if __name__ == '__main__':
    od = OrderedList()
    od.add(2)
    od.add(4)
    od.add(1)
    od.add(7)
    od.add(5)
    od.add(0)
    od.add(9)

    print(od)
