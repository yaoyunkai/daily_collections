"""

牛顿法求平方根

created at 2025/3/22
"""

from decimal import Decimal, getcontext


def sqrt_newton(a, precision=100):
    getcontext().prec = precision + 2  # 额外保留2位防止舍入误差
    a = Decimal(a)
    x = a  # 初始猜测值
    while True:
        new_x = (x + a / x) / 2
        if abs(new_x - x) < Decimal(10) ** (-precision):
            break
        x = new_x
    getcontext().prec = precision
    return +new_x  # 触发舍入到目标精度


if __name__ == '__main__':
    # 计算√2的前100位小数
    result = sqrt_newton(2, 100)
    print(f"√2 = {result}")
