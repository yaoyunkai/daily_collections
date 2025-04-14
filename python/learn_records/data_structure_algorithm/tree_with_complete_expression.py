"""
完全括号表达式 Fully Parenthesized Expression

左括号，右括号，操作数和计算符

created at 2025/4/14
"""
import operator

from binary_tree import BinaryTree
from stack import Stack


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


def tokenize(fp_exp: str):
    tokens = []
    current_token = ""
    # 将表达式拆分为 token（处理多位数和运算符）
    for char in fp_exp:
        if char in "()+-*/":
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(char)
        elif char.isdigit():
            current_token += char
        else:
            if current_token:
                tokens.append(current_token)
                current_token = ""
    if current_token:
        tokens.append(current_token)

    return tokens


def tokenize_with_negative(fp_exp: str):
    tokens = []
    current_token = ""
    # 改进后的 token 化逻辑，支持负数和多位数
    for i, char in enumerate(fp_exp):
        if char in "()+-*/":
            # 处理负数的情况
            if char == '-' and (i == 0 or (i > 0 and fp_exp[i - 1] in "()+-*/")):
                # 负号前是运算符或括号，或在开头，视为负数的一部分
                current_token += char
            else:
                # 普通运算符或括号，提交当前 token
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                tokens.append(char)
        elif char.isdigit():
            current_token += char
        else:
            # 忽略空格或其他字符（根据需求调整）
            continue

    # 提交最后一个 token
    if current_token:
        tokens.append(current_token)

    return tokens


def build_tree(fp_exp: str):
    """
    不支持小数点

    """
    tokens = tokenize_with_negative(fp_exp)

    stack = Stack()
    tree = BinaryTree('')
    current_tree = tree

    stack.push(tree)

    for token in tokens:
        if token == '(':
            current_tree.insert_left('')
            stack.push(current_tree)
            current_tree = current_tree.get_left_child()
        elif token in '+-*/':
            current_tree.set_root_value(token)
            current_tree.insert_right('')
            stack.push(current_tree)
            current_tree = current_tree.get_right_child()
        elif token == ')':
            current_tree = stack.pop()
        else:
            # 处理操作数（包括负数）
            # current_tree.set_root_value(eval(token))
            current_tree.set_root_value(int(token))
            current_tree = stack.pop()

    return tree


def evaluate(parse_tree: BinaryTree):
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }

    left_child = parse_tree.get_left_child()
    right_child = parse_tree.get_right_child()

    if left_child and right_child:
        fn = operators[parse_tree.get_root_val()]
        return fn(evaluate(left_child), evaluate(right_child))
    else:
        return parse_tree.get_root_val()


def post_order_eval(tree: BinaryTree):
    """
    中序遍历求解析式的值

    """
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }

    if tree:
        res1 = post_order_eval(tree.get_left_child())
        res2 = post_order_eval(tree.get_right_child())
        if res1 and res2:
            return operators[tree.get_root_val()](res1, res2)
        else:
            return tree.get_root_val()


def evaluate_parse_tree(node):
    # 空节点处理（根据需求可抛出异常）
    if node is None:
        return 0

    # 叶子节点：返回数值
    if node.left_child is None and node.right_child is None:
        return node.key

    # 递归计算左右子树
    left_val = evaluate_parse_tree(node.left_child)
    right_val = evaluate_parse_tree(node.right_child)

    # 根据运算符计算结果
    opt = node.key
    if opt == '+':
        return left_val + right_val
    elif opt == '-':
        return left_val - right_val
    elif opt == '*':
        return left_val * right_val
    elif opt == '/':
        if right_val == 0:
            raise ValueError("除数不能为零")
        return left_val / right_val
    else:
        raise ValueError(f"未知运算符: {opt}")


def print_fp_exp(tree: BinaryTree):
    """
    (((-3)+((4)*(55)))-((2)/(1)))

    TODO 移除括号

    """
    s_val = ''
    if tree:
        s_val = '(' + print_fp_exp(tree.get_left_child())
        s_val = s_val + str(tree.get_root_val())
        s_val = s_val + print_fp_exp(tree.get_right_child()) + ')'

    return s_val


if __name__ == '__main__':
    # exp = '((7+3)*(5-2))'
    # root_node = build_parse_tree(exp)
    # root_node.pretty_print()

    exp2 = "((3 + (4 * 5)) - (2 / 1))"
    exp3 = "((3 + (4 * 55)) - (2 / 1))"
    exp4 = "((-3 + (4 * 55)) - (2 / 1))"
    exp5 = "((-35 + 10) * (27 - 4))"
    build_tree(exp2)
    build_tree(exp3)
    obj1 = build_tree(exp4)
    obj2 = build_tree(exp5)

    # obj2.pretty_print()
    obj1.pretty_print()

    print(evaluate(obj1))
    print(evaluate_parse_tree(obj1))
    print(post_order_eval(obj1))

    print(print_fp_exp(obj1))
