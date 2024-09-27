"""

1. Vector 向量



created at 2024/9/27
"""

import numpy as np


def demo1():
    a = np.array([[-3, 1], [2, 5]])
    b = np.array([[5, 3], [7, -3]])

    print(a * b)
    print(a.dot(b))


def vector_compute():
    """
    Vector Operations
    arrows in space

    x-axis
    y-axis



    """
    a = np.array([3, -5])
    b = np.array([2, 1])
    print(a + b)
    print(2 * a)


def matrix_operations():
    a = np.array([[1, -3], [2, 4]])
    b = np.array([5, 7])

    print(a * b)
    print()

    # 矩阵向量乘法
    print(a.dot(b, ))

    # 两个矩阵相乘
    c = [[1, 1], [0, 1]]
    d = [[0, -1], [1, 0]]
    print(np.dot(c, d))
    print(np.dot(d, c))

    # 线性变换的行列式
    e = [[3, 2], [0, 2]]
    print(np.linalg.det(e))


if __name__ == '__main__':
    # demo1()
    # vector_compute()
    matrix_operations()
