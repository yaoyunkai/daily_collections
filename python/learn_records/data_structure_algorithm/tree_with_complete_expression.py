"""
完全表达式

左括号，右括号，操作数和计算符

created at 2025/4/14
"""

from stack import Stack
from tree_demo import BinaryTree


def build_parse_tree(fpexp: str):
    fp_list = fpexp.split()
    p_stack = Stack()
    e_tree = BinaryTree('')
    p_stack.push(e_tree)

    current_tree = e_tree

    for i in fp_list:
        if i == '(':
            current_tree.insert_left('')
            p_stack.push(current_tree)
            current_tree = current_tree.get_left_child()

        elif i not in '+-*/)':
            current_tree.set_root_value(eval(i))
            # current_tree.set_root_value(i)
            parent = p_stack.pop()
            current_tree = parent

        elif i in '+-*/':
            current_tree.set_root_value(i)
            current_tree.insert_right('')
            p_stack.push(current_tree)
            current_tree = current_tree.get_right_child()

        elif i == ')':
            current_tree = p_stack.pop()
        else:
            raise ValueError(f'Unknown operator: {i}')

    return e_tree


if __name__ == '__main__':
    exp = '((7+3)*(5-2))'

    root_node = build_parse_tree(exp)
    root_node.pretty_print()
