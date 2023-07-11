"""
Created at 2023/7/9


"""

from anytree import Node, RenderTree
from anytree.exporter import DotExporter


def simple_usage():
    udo = Node("Udo")
    marc = Node("Marc", parent=udo)
    lian = Node("Lian", parent=marc)
    dan = Node("Dan", parent=udo)
    jet = Node("Jet", parent=dan)
    jan = Node("Jan", parent=dan)
    joe = Node("Joe", parent=dan)

    for pre, _, node in RenderTree(udo):
        print("%s%s" % (pre, node.name))

    # DotExporter(udo).to_picture('udo.png')


if __name__ == '__main__':
    simple_usage()
