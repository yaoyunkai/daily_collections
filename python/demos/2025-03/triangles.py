"""


created at 2025/3/29
"""


def is_triangle(a, b, c):
    # 计算向量AB和向量AC的行列式（叉积）
    area_twice = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return area_twice != 0


def calculate_triangle_area(a, b, c):
    """
    计算三个点构成的三角形面积。若三点共线，返回0。

    参数:
    a, b, c -- 三个点的坐标，格式为元组或列表，例如 (x, y)

    返回:
    三角形面积（浮点数）
    """
    # 计算向量AB和向量AC的叉积（两倍面积）
    area_twice = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return abs(area_twice) / 2.0


if __name__ == '__main__':
    pass
