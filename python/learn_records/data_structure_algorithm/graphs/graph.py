"""

图的实现， 接邻矩阵和接邻表

无向图

created at 2025/4/16
"""

from utils import count_digits


class BagIterator:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.start is None:
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
    """
    接邻表

    所有顶点保存为一个主列表。
    为每个顶点对象都维护一个列表，其中记录了与它相连的顶点。
    {V, weight}

    一般使用0至V-1来表示一张含有V个顶点的图中的各个顶点


    """

    V = 0  # 顶点数
    E = 0  # 边的数量
    adj: list[Bag]  # 接邻表

    # def __init__(self):
    #     raise NotImplementedError("can't directly create Graph instance")

    @classmethod
    def create_graph_from_vertices(cls, v: int):
        """
        8个顶点就是 0-7.

        """
        if v < 0:
            raise ValueError("Number of vertices must be non-negative")
        obj = cls()
        obj.V = v
        obj.E = 0
        obj.adj = list()

        for i in range(obj.V):
            obj.adj.append(Bag())

        return obj

    @classmethod
    def create_graph_from_text(cls, filename) -> "Graph":
        """
        格式:
            顶点数  如 15, 那么v 和 w的取值范围只能是0-14
            边的数
            v -> w
            v -> w

        """

        obj = cls()

        with open(filename, mode="r", encoding="utf8") as fp:
            obj.V = int(fp.readline())
            if obj.V < 0:
                raise ValueError("Number of vertices must be non-negative")

            obj.adj = list()
            for i in range(obj.V):
                obj.adj.append(Bag())

            lines = int(fp.readline())

            if obj.E < 0:
                raise ValueError("number of edges in a Graph must be non-negative")

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
        self.adj[v].add(w)
        self.adj[w].add(v)

    def degree(self, v):
        self._validate_vertex(v)
        return self.adj[v].size()

    def max_degree(self) -> int:
        max_d = 0
        for v in range(self.V):
            max_d = max(max_d, self.degree(v))
        return max_d

    def avg_degree(self):
        return 2 * self.E / self.V

    def __str__(self):
        exp = "{0:%sd}: " % (count_digits(self.V))

        string = f"{self.V} vertices, {self.E} edges \n"
        for i in range(self.V):
            string += exp.format(i)
            string += " ".join([str(item) for item in self.adj[i]])
            string += "\n"

        return string

    def to_dot(self):
        """
        dot input.dot -Tsvg -o output.svg
        dot input.dot -Tpdf -o output.pdf

        """
        str_list = list()
        str_list.append("graph {")
        str_list.append("\n")
        str_list.append('node[shape=circle, style=filled, fixedsize=true, width=0.3, fontsize="10pt"]')
        str_list.append("\n")

        self_loops = 0

        for i in range(self.V):
            for item in self.adj[i]:
                if i < item:
                    str_list.append(f"{i} -- {item}\n")
                elif i == item:
                    if self_loops % 2 == 0:
                        str_list.append(f"{i} -- {item}\n")
                    self_loops += 1

        str_list.append("}\n")

        return "".join(str_list)

    def get_v(self):
        return self.V

    def get_e(self):
        return self.E


if __name__ == "__main__":
    # graph = Graph.create_graph_from_vertices(10)
    graph = Graph.create_graph_from_text("data/tinyG.txt")
    print(graph)
