"""
递归可视化

turtle package

created at 2025/4/9
"""
from turtle import Turtle, exitonclick

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


def draw_tree():
    my_turtle.left(90)
    my_turtle.up()
    my_turtle.backward(300)
    my_turtle.down()
    my_turtle.color('green')
    tree(110, my_turtle)


def draw_triangle(points, color, t: Turtle):
    t.fillcolor(color)
    t.up()
    t.goto(points[0])
    t.down()
    t.begin_fill()
    t.goto(points[1])
    t.goto(points[2])
    t.goto(points[0])
    t.end_fill()


def get_mid(p1, p2):
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2


def sierpinski(points, degree, t: Turtle):
    colormap = ['blue', 'red', 'green', 'white', 'yellow', 'violet', 'orange']
    draw_triangle(points, colormap[degree], t)

    if degree > 0:
        sierpinski([points[0], get_mid(points[0], points[1]), get_mid(points[0], points[2])], degree - 1, t)
        sierpinski([points[1], get_mid(points[0], points[1]), get_mid(points[1], points[2])], degree - 1, t)
        sierpinski([points[2], get_mid(points[2], points[1]), get_mid(points[0], points[2])], degree - 1, t)


def draw_final():
    my_points = [(-500, -250), (0, 500), (500, -250)]
    sierpinski(my_points, 5, my_turtle)


if __name__ == '__main__':
    # draw_spiral(my_turtle, 100)

    # draw_tree()

    draw_final()
    # 等待用户点击后关闭窗口
    exitonclick()
