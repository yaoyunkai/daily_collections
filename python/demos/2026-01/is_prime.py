"""
write your description here.

"""


def is_prime(n):
    if n < 2:  # 0和1不是素数
        return False
    if n == 2 or n == 3:  # 2和3是素数
        return True
    if n % 2 == 0 or n % 3 == 0:  # 排除偶数和3的倍数
        return False

    # 只用检查 6k±1 的数就可以了
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


# 测试
print(is_prime(55555555555551))  # True
print(is_prime(18))  # False
print(is_prime(1))  # False
print(is_prime(2))  # True
