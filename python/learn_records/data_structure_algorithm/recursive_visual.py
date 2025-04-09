"""
递归可视化

turtle package

created at 2025/4/9
"""
from turtle import *

my_turtle = Turtle()


def draw_spiral(turtle_obj, line_len):
    if line_len > 0:
        turtle_obj.forward(line_len)
        turtle_obj.right(90)
        draw_spiral(turtle_obj, line_len - 5)


def tree(branch_len, t: Turtle):
    if branch_len > 5:
        t.forward(branch_len)
        t.right(20)
        tree(branch_len - 15, t)
        t.left(40)
        tree(branch_len - 10, t)
        t.right(20)
        t.backward(branch_len)


if __name__ == '__main__':
    # draw_spiral(my_turtle, 100)

    my_turtle.left(90)
    my_turtle.up()
    my_turtle.backward(300)
    my_turtle.down()
    my_turtle.color('green')
    tree(110, my_turtle)

    # 等待用户点击后关闭窗口
    exitonclick()
