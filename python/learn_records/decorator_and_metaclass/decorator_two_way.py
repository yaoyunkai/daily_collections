"""


Created at 2023/6/28
"""

def func(arg=None):
    # 判断是否传递了参数
    if arg is not None:
        # 如果传递了参数，返回装饰器函数
        def decorator(original_func):
            def wrapper():
                # 在函数执行前的操作
                print(f"在函数执行前，参数值为: {arg}")

                # 调用原始函数
                original_func()

                # 在函数执行后的操作
                print("在函数执行后")

            return wrapper
        return decorator
    else:
        # 如果没有传递参数，直接执行装饰器逻辑
        def wrapper(original_func):
            # 在函数执行前的操作
            print("在函数执行前")

            # 调用原始函数
            original_func()

            # 在函数执行后的操作
            print("在函数执行后")
        return wrapper

# 使用装饰器的两种形式

# 形式1: @func(params=123)
@func(params=123)
def test1():
    print("test1() 函数被调用")

test1()

print("---")

# 形式2: @func
@func
def test2():
    print("test2() 函数被调用")

test2()
