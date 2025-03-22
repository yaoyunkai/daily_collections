"""


created at 2025/3/22
"""

from decimal import Decimal, getcontext, setcontext, ExtendedContext


def compute_pi_chudnovsky(precision):
    # 设置临时精度高于目标精度，避免中间计算溢出
    setcontext(ExtendedContext)
    getcontext().prec = precision * 2  # 临时提升精度（例如 200 位）

    C = 426880 * Decimal(10005).sqrt()
    K = Decimal(6)
    M = Decimal(1)
    X = Decimal(1)
    L = Decimal(13591409)
    S = L

    # 根据精度需求动态调整迭代次数（每次迭代增加约14位有效数字）
    iterations = (precision // 14) + 1

    for i in range(1, iterations):
        # 更新 M：使用整数运算避免浮点误差
        M = (K ** 3 - 16 * K) * M // (-262537412640768000 * i ** 3)

        # 更新 L 和 X
        L += 545140134
        X *= -262537412640768000

        # 计算当前项并累加
        term = (M * L) / X
        S += term
        K += 12

    # 计算最终 π 值
    _pi = C / S

    # 重置精度为目标精度并返回结果
    getcontext().prec = precision + 1  # 1位整数 + 100位小数
    return +_pi  # 触发舍入


if __name__ == '__main__':
    # 计算小数点后100位
    LEN = 100

    pi = compute_pi_chudnovsky(LEN)
    pi_str = str(pi)
    decimal_part = pi_str.split('.')[1][:LEN]

    print(f"圆周率的小数点后100位是：\n{decimal_part}")
