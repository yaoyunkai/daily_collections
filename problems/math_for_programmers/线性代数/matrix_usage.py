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


def matrix_operations2():
    a = np.array([[1, -3], [2, 4]])
    inverse_a = np.linalg.inv(a)
    # inv_a = np.array([[4, 3], [2, 1]])

    print(a)
    print(inverse_a)

    print(a.dot(inverse_a))

    c = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 10]
    ])
    # 求矩阵的秩
    matrix_rank = np.linalg.matrix_rank(c)
    print("矩阵的秩为:", matrix_rank)


def matrix_operations3():
    # 创建一个矩阵A
    A = np.array([[1, 2], [3, 4]])

    # 创建一个向量v
    v = np.array([1, 2])

    # 使用dot函数进行矩阵和向量相乘
    result = np.dot(A, v)
    print(result)

    # 创建两个向量
    vector1 = np.array([2, 0])
    vector2 = np.array([0, 2])

    # 使用numpy.dot计算点乘
    dot_product = np.dot(vector1, vector2)
    print(dot_product)  # 输出结果应为32

    v3 = np.array([1, 1])
    v4 = np.array([2, -2])
    print(np.dot(v3, v4))


def matrix_operations4():
    a = np.array([2, 2])
    b = np.array([-1, 1])
    # 叉积
    print(np.cross(a, b))

    c = np.array([1, 2, 3])
    d = np.array([4, 5, 6])
    # 向量的长度表示 c d的叉积
    print(np.cross(c, d))

    # a1 = np.array([[2, -1], [1, 1]])
    # print(np.linalg.inv(a1))


def matrix_operations5():
    """
    特征值和特征向量

    """
    a = np.array([[0.5, -1.0], [-1.0, 0.5]])

    res1 = np.linalg.eig(a)
    print(res1)


if __name__ == '__main__':
    # demo1()
    # vector_compute()
    # matrix_operations2()
    # matrix_operations3()
    matrix_operations5()
