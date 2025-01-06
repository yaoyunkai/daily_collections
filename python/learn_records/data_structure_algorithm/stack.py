"""
匹配括号
进制转换

前序 中序 后序 表达式 / 完全括号表达式


created at 2025/1/6
"""


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


if __name__ == '__main__':
    rr = dec_to_str(31, base=15)
    print(rr)
