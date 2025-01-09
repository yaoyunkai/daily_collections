"""
匹配括号
进制转换

前序 中序 后序 表达式 / 完全括号表达式


created at 2025/1/6
"""
import string


class Stack:
    def __init__(self):
        self.__data = []

    def __len__(self):
        return len(self.__data)

    def size(self):
        return len(self.__data)

    def push(self, item):
        self.__data.append(item)

    def pop(self):
        return self.__data.pop()

    def peek(self):
        return self.__data[-1]

    def is_empty(self):
        return len(self.__data) == 0


def par_check(val: str):
    right = {
        ')': '(',
        '}': '{',
        ']': '[',
    }
    left = ['(', '[', '{']

    stack = Stack()

    for char in val:
        if char in left:
            stack.push(char)
        elif char in right:
            if stack.is_empty() or stack.pop() != right[char]:
                return False

    return stack.is_empty()


def dec_to_str(val: int, *, base=2):
    """
    2 8 16
    """
    if not 2 <= base <= 16:
        raise ValueError('invalid base number, must be 2, 8, 16')

    stack = Stack()

    while val > 0:
        rem = val % base
        if rem == 10:
            rem = 'A'
        elif rem == 11:
            rem = 'B'
        elif rem == 12:
            rem = 'C'
        elif rem == 13:
            rem = 'D'
        elif rem == 14:
            rem = 'E'
        elif rem == 15:
            rem = 'F'
        else:
            rem = str(rem)

        stack.push(rem)
        val = val // base

    result = ''
    while not stack.is_empty():
        result += stack.pop()
    return result


prec = {
    '*': 3,
    '/': 3,
    '+': 2,
    '-': 2,
    '(': 1,
}


def infix_to_postfix(infix_expr: str):
    op_stack = Stack()
    postfix_list = []
    token_list = infix_expr.split()

    for token in token_list:
        if token in string.ascii_uppercase:
            postfix_list.append(token)
        elif token == '(':
            op_stack.push(token)
        elif token == ')':
            top_token = op_stack.pop()

            while top_token != '(':
                postfix_list.append(top_token)
                top_token = op_stack.pop()
        else:
            while (not op_stack.is_empty()) and (prec[op_stack.peek()] >= prec[token]):
                postfix_list.append(op_stack.pop())

            op_stack.push(token)

    while not op_stack.is_empty():
        postfix_list.append(op_stack.pop())

    return ' '.join(postfix_list)


def postfix_eval(postfix_expr: str):
    operand_stack = Stack()

    token_list = postfix_expr.split()

    for token in token_list:
        if token in string.digits:
            operand_stack.push(int(token))
        else:
            op2 = operand_stack.pop()
            op1 = operand_stack.pop()
            result = do_math(token, op1, op2)
            operand_stack.push(result)

    return operand_stack.pop()


def do_math(op, op1, op2):
    if op == '*':
        return op1 * op2
    elif op == '/':
        return op1 / op2
    elif op == '+':
        return op1 + op2
    else:
        return op1 - op2


if __name__ == '__main__':
    print(infix_to_postfix('A + B * C'))
    print(postfix_eval('4 5 6 * +'))
