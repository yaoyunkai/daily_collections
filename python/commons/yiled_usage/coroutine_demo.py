"""

inspect.getgeneratorstate

GEN_CREATED
GEN_RUNNING
GEN_SUSPENDED
GEN_CLOSED


Created at 2023/3/30
"""
import inspect
import time


def simple_coroutine():
    x = -1
    print('-> coroutine started')
    while True:
        x = yield x
        # if type(x) is not int:
        #
        #     print(inspect.getgeneratorstate(x))
        #     x.send(56)
        print('-> coroutine received: ', x)
        time.sleep(3)


if __name__ == '__main__':
    # for i in simple_coroutine():
    #     print('---> ', i)
    #
    # i = iter(simple_coroutine())
    # for item in i:
    #     print(item)

    g = simple_coroutine()
    print(g)

    ret = next(g)  # 先激活 generator此时 ret = -1, 协程暂停在 yield, = 左边的x等着下一个send
    print(ret)

    print(inspect.getgeneratorstate(g))  # GEN_SUSPENDED

    # 左边的x 接收到 42 , 然后打印, 然后sleep 3s, 再次暂停在yield, x此时已经是42了,所以ret是42
    ret = g.send(42)
    print(ret)

    ret = g.send(g)  # 左边的x 接收到 43 , 然后打印, 然后sleep 3s, 再次暂停在yield, x此时已经是43了,所以ret是43
    print(ret)

    print(inspect.getgeneratorstate(g))  # GEN_SUSPENDED
