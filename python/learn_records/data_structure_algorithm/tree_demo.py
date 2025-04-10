"""

树的定义

created at 2025/4/10
"""


class BinaryTree:
    def __init__(self, root_node):
        self.key = root_node
        self.left_child = None
        self.right_child = None

    def insert_left(self, new_node):
        if self.left_child is None:
            self.left_child = self.__class__(new_node)
        else:
            t = self.__class__(new_node)
            t.left_child = self.left_child
            self.left_child = t

    def insert_right(self, new_node):
        if self.right_child is None:
            self.right_child = self.__class__(new_node)
        else:
            t = self.__class__(new_node)
            t.right_child = self.right_child
            self.right_child = t

    def get_right_child(self):
        return self.right_child

    def get_left_child(self):
        return self.left_child

    def set_root_value(self, obj):
        self.key = obj

    def get_root_val(self):
        return self.key

    def pretty_print(self):
        """Pretty print the binary tree structure."""

        def _pretty(node, prefix="", is_last=True):
            if node is None:
                return ""
            curr_str = ""
            # 根据是否是最后一个子节点，选择符号
            if is_last:
                curr_str += prefix + "└── " + str(node.key) + "\n"
                new_prefix = prefix + "    "  # 最后一个子节点，后续无需竖线
            else:
                curr_str += prefix + "├── " + str(node.key) + "\n"
                new_prefix = prefix + "│   "  # 非最后一个子节点，后续需要竖线

            # 收集子节点，先左后右
            children = []
            if node.left_child:
                children.append(node.left_child)
            if node.right_child:
                children.append(node.right_child)

            # 递归处理子节点，最后一个子节点标记为is_last=True
            for i, child in enumerate(children):
                curr_str += _pretty(child, new_prefix, i == len(children) - 1)
            return curr_str

        print(_pretty(self))


if __name__ == '__main__':
    # 构建示例二叉树
    root = BinaryTree('A')
    root.insert_left('B')
    root.insert_right('C')
    root.left_child.insert_left('D')
    root.left_child.insert_right('E')
    root.right_child.insert_left('F')
    root.right_child.insert_right('G')

    # 打印树结构
    root.pretty_print()
