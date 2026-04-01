"""
from books

"""


class Vertex:
    def __init__(self, key):
        self.id = key
        self.connected_to = {}

    def add_neighbor(self, nbr, weight):
        self.connected_to[nbr] = weight

    def __str__(self):
        return f"{self.id} connected to {[x.id for x in self.connected_to]}"

    def get_connections(self):
        return self.connected_to.keys()

    def get_id(self):
        return self.id

    def get_weight(self, nbr, default=None):
        return self.connected_to.get(nbr, default)


class Graph:
    def __init__(self):
        self.vert_list = {}
        self.num_vertices = 0

    def add_vertex(self, key):
        self.num_vertices += 1
        new_vertex = Vertex(key)
        self.vert_list[key] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        return self.vert_list.get(n)

    def __contains__(self, n):
        return n in self.vert_list

    def add_edge(self, front, tail, weight):
        if front not in self:
            self.add_vertex(front)
        if tail not in self:
            self.add_vertex(tail)

        self.vert_list[front].add_neighbor(self.vert_list[tail], weight)

    def get_vertices(self):
        return self.vert_list.keys()
