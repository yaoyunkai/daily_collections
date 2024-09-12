"""


created at 2024/9/12
"""
import matplotlib.pyplot as plt
import numpy as np
from sympy import Symbol
from sympy import solve


def resolve_equation():
    """
    求a+b=90 a/b=17的解

    """
    a = Symbol("a")
    b = Symbol("b")
    result = solve([a + b - 90, a / b - 17], [a, b])
    print(result)


def display():
    plt.figure(1, figsize=(5, 5), facecolor='w', edgecolor='w', dpi=100, frameon=True)
    line1_a = np.linspace(0, 100, 100)
    line1_b = 90 - line1_a

    line2_a = np.linspace(0, 100, 100)
    line2_b = line2_a / 17

    plt.plot(line1_a, line1_b, color='b', label='a+b=90')
    plt.plot(line2_a, line2_b, color='r', label='a/b=17')

    # 再添加一些网格线坐标轴之类的细节
    for i in range(0, 100, 5):
        x = np.linspace(0, 100, 100)
        y = x * 0 + i
        plt.plot(x, y, color="magenta", linestyle=":", linewidth=0.5)

    for j in range(0, 100, 5):
        y = np.linspace(0, 100, 100)
        x = y * 0 + j
        plt.plot(x, y, color="magenta", linestyle=":", linewidth=0.5)

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel("A", fontsize=15, labelpad=0, horizontalalignment='right', x=0.5)
    plt.ylabel("B", fontsize=15, labelpad=0, horizontalalignment='right', x=0.5)
    plt.xticks(color="indianred")
    plt.xticks(range(0, 100, 5))
    plt.xlim(0, 100)
    plt.yticks(color="indianred")
    plt.yticks(range(0, 100, 5))
    plt.ylim(0, 100)
    plt.title("resolve equation")

    plt.legend(bbox_to_anchor=(0.74, 0.865))
    bbox_args = dict(boxstyle="round", fc="lightgreen")
    arrow_args = dict(arrowstyle="->", color='g')
    plt.annotate("(易得交叉点为(85,15))",
                 xy=(86, 6),
                 xytext=(20, 20),
                 ha="left", va="bottom",
                 bbox=bbox_args,
                 arrowprops=dict(connectionstyle="arc3,rad=-0.2", **arrow_args, )
                 )

    plt.show()


if __name__ == '__main__':
    # resolve_equation()
    display()
