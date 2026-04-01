"""

Search(Graph G, int S)  find all Node that connected to S

marked(int v)  v 和 S 是否连通。
count()      与s 连通的顶点总数。


深度优先搜索

但图的许多其他性质和路径有关，因此一种很自然的想法是沿着图的边从一个顶点移动到另一个顶点。

=====================================================

走迷宫

Tremaux搜索



created at 2025/4/17
"""

from graph import Graph


class DepthFirstSearch:
    marked: list[bool]
    count: int

    def __init__(self, graph: Graph, s):
        self.marked = [False for _ in graph.get_v()]
        self.count = 0
        self._validate_vertex(s)
        self._dfs(graph, s)

    def _dfs(self, graph: Graph, v):
        self.count += 1
        self.marked[v] = True

        for w in graph.adj[v]:
            if not self.marked[w]:
                self._dfs(graph, w)

    def _validate_vertex(self, v):
        lens = len(self.marked)
        if v < 0 or v >= lens:
            raise ValueError("invalid v")

    def is_marked(self, v):
        self._validate_vertex(v)
        return self.marked[v]

    def get_count(self):
        return self.count
