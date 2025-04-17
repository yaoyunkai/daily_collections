"""

图算法

图是由一组顶点和一组能够将两个顶点相连的边组成的。

一般使用0至V-1来表示一张含有V个顶点的图中的各个顶点

我们用v-w的记法来表示连接v和w的边，w-v是这条边的另一种表示方法

自环  一条连接一个顶点和其自身的边；

        连接同一对顶点的两条边称为平行边。


相邻顶点
顶点的度数： 某个顶点的度数即为依附于它的边的总数。


在图中，路径是由边顺序连接的一系列顶点。
简单路径是一条没有重复顶点的路径。
环是一条至少含有一条边且起点和终点相同的路径。
简单环是一条（除了起点和终点必须相同之外）不含有重复顶点和边的环。
路径或者环的长度为其中所包含的边数。

如果从任意一个顶点都存在一条路径到达另一个任意顶点，我们称这幅图是连通图。


created at 2025/4/16
"""


class BagIterator:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        return self

    def __next__(self):
        if not self.start:
            raise StopIteration
        _item = self.start.value
        self.start = self.start.next
        return _item


class BagNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class Bag:
    def __init__(self):
        self.first = None
        self.n = 0

    def __iter__(self):
        return BagIterator(self.first)

    def is_empty(self):
        return self.first is None

    def size(self):
        return self.n

    def add(self, item):
        old = self.first
        new_node = BagNode(item)
        new_node.next = old
        self.first = new_node
        self.n += 1

    def search(self, item):
        cur: BagNode = self.first
        while cur is not None:
            if cur.value == item:
                return True
            cur = cur.next
        return False


class Graph:
    V = 0  # 顶点数
    E = 0  # 边的数量
    adj = None  # 接邻表

    @classmethod
    def create_graph_from_vertices(cls, v: int):
        if v < 0:
            raise ValueError('Number of vertices must be non-negative')
        obj = cls()
        obj.V = v
        obj.E = 0
        obj.adj = list()

        for i in range(obj.V):
            obj.adj.append(list())

        return obj

    @classmethod
    def create_graph_from_text(cls, filename) -> 'Graph':
        obj = cls()

        with open(filename, mode='r', encoding='utf8') as fp:
            obj.V = int(fp.readline())
            if obj.V < 0:
                raise ValueError('Number of vertices must be non-negative')

            obj.adj = list()
            for i in range(obj.V):
                obj.adj.append(list())

            lines = int(fp.readline())

            if obj.E < 0:
                raise ValueError('number of edges in a Graph must be non-negative')

            for i in range(lines):
                _tmp = fp.readline().split()
                left, right = int(_tmp[0]), int(_tmp[1])
                obj.add_edge(left, right)

        return obj

    def _validate_vertex(self, value):
        if not 0 <= value < self.V:
            raise ValueError(f"vertex {value} is not between 0 and {self.V - 1}")

    def add_edge(self, v, w):
        self._validate_vertex(v)
        self._validate_vertex(w)
        self.E += 1
        self.adj[v].append(w)
        self.adj[w].append(v)

    # def __str__(self):
    #     string = f'{self.V} vertices, {self.E} edges \n'


if __name__ == '__main__':
    # graph = Graph.create_graph_from_vertices(10)
    graph = Graph.create_graph_from_text('tinyG.txt')
    print(graph)
