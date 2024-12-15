"""

画 y = x/(x+100) 的图像


"""

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import rcParams

rcParams['font.sans-serif'] = ['Microsoft Yahei', 'SimHei']  # 使用黑体
rcParams['axes.unicode_minus'] = False  # 避免坐标轴负号显示问题


def cooldown(x):
    return x / (x + 100) * 100


def draw_x_y():
    x = np.linspace(0, 500, 1000)
    y = cooldown(x)

    plt.plot(x, y)
    plt.xlabel('技能急速 (x)')
    plt.ylabel('冷却缩减 (y)')
    plt.title('y = x / (x + 100)')
    plt.grid(True)

    # 标注某个点
    bbox_args = dict(boxstyle="round", fc="lightgreen")
    arrow_args = dict(arrowstyle="->", color='g')
    plt.annotate("A",
                 xy=(50, cooldown(50)),
                 xytext=(20, 20),
                 # ha="right",
                 # va="bottom",
                 bbox=bbox_args,
                 arrowprops=dict(connectionstyle="arc3,rad=-0.2", **arrow_args))

    plt.show()


if __name__ == '__main__':
    draw_x_y()
