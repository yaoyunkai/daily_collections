"""

Introduce:

    子生成器产出的值都直接传给委派生成器的调用方

    使用 send() 方法发给委派生成器的值都直接传给子生成器

    生成器退出时，生成器（或子生成器）中的 return expr 表达式会触发 StopIteration(expr) 异常抛出。

    yield from 表达式的值是子生成器终止时传给 StopIteration 异常的第一个参数。


yield from 结构的另外两个特性与异常和终止有关
    传入委派生成器的异常，除了 GeneratorExit 之外都传给子生成器的 throw() 方法

    如果把 GeneratorExit 异常传入委派生成器，或者在委派生成器
    上调用 close() 方法，那么在子生成器上调用 close() 方法，如果它有的话。


Created at 2023/3/31
"""
import random

random.seed(0)


class Stop:
    pass


def gen_01():
    print('gen_01 started')
    x = None

    while True:
        recv = yield x
        print('recv data : {}'.format(recv))
        if isinstance(recv, Stop):
            print('recv stop flag...')
            break

        x = random.choice([5, 3, 4, 6, 9, 10])

    return 9999


def handler():
    print('start handler')
    ret1 = yield from gen_01()
    print(ret1)

    ret1 = yield from gen_01()
    print(ret1)
    print('end handler')


if __name__ == '__main__':
    cor = handler()
    cor.send(None)  # 预激委派生成器, 委派生成器会自动启动子生产器

    rr = cor.send(45)
    print('Get ret: %s' % rr)

    rr = cor.send(33)
    print('Get ret: %s' % rr)

    """
    如果在委派生成器中，只有一个 yield from, 那么会引发 StopIteration 异常
    所以在执行这一半的时候 cor.send(Stop()) 就 raise error 了
    
    如果在委派生成器中，还有 yield from, 那么当第一个子生成器停止后,会激活下一个
    子生成器。
    会执行到子生成器中的第一个yield from的右边停下
    
    """
    rr = cor.send(Stop())
    print('Get ret: %s' % rr)

    rr = cor.send(56)
    print('Get ret: %s' % rr)
