"""
(1) 递归算法必须有基本情况；
(2) 递归算法必须改变其状态并向基本情况靠近；
(3) 递归算法必须递归地调用自己。

created at 2025/4/9
"""
import timeit

from stack import Stack


def list_num(num_list: list):
    cnt = 0

    for i in num_list:
        cnt += i

    return cnt


def list_num_rec(num_list: list):
    if len(num_list) == 1:
        return num_list[0]
    else:
        return num_list[0] + list_num_rec(num_list[1:])


def to_str(n, base: int):
    convert_string = '0123456789ABCDEF'

    if not 2 <= base <= 16:
        raise ValueError('base must be in 2~16')

    if n < base:
        return convert_string[n]
    else:
        return to_str(n // base, base) + convert_string[n % base]


def to_str_stack(n_out, base_out):
    r_stack = Stack()

    def _to_str_stack(n, base):
        convert_string = '0123456789ABCDEF'
        if not 2 <= base <= 16:
            raise ValueError('base must be in 2~16')

        if n < base:
            r_stack.push(convert_string[n])
        else:
            r_stack.push(convert_string[n % base])
            _to_str_stack(n // base, base)

    _to_str_stack(n_out, base_out)

    print(r_stack)


def to_str_with_dbg(n, base: int, level=0):
    convert_string = '0123456789ABCDEF'
    indent = '    ' * level  # 用缩进表示递归深度

    print(f"{indent}--> to_str(n={n}, base={base})")

    if not 2 <= base <= 16:
        raise ValueError('base must be in 2~16')

    if n < base:
        result = convert_string[n]
        print(f"{indent}<< return {result}")
        return result
    else:
        quotient = n // base
        remainder = n % base
        # 递归调用时层级+1
        recursive_result = to_str_with_dbg(quotient, base, level + 1)
        current_result = recursive_result + convert_string[remainder]
        print(f"{indent}<< {recursive_result} + {convert_string[remainder]} = {current_result}")
        return current_result


def test_cost():
    # 测试数据（示例中使用长度为 100 的列表）
    test_list = list(range(100))

    # 测量循环版本
    time_loop = timeit.timeit(lambda: list_num(test_list), number=1000)
    print(f"循环版本执行时间：{time_loop:.6f} 秒")

    # 测量递归版本
    time_recursion = timeit.timeit(lambda: list_num_rec(test_list), number=1000)
    print(f"递归版本执行时间：{time_recursion:.6f} 秒")


if __name__ == '__main__':
    print(to_str_with_dbg(45, 2))

    to_str_stack(45, 8)
