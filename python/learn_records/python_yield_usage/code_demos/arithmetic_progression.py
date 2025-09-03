"""
ArithmeticProgression

"""
import itertools


def aritprog_gen(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    if end is None:
        return ap_gen
    return itertools.takewhile(lambda n: n < end, ap_gen)


class ArithmeticProgression:
    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end

    def __iter__(self):
        res_type = type(self.begin + self.step)
        result = res_type(self.begin)

        forever = self.end is None
        idx = 0

        while forever or result < self.end:
            yield result
            idx += 1
            """
            没有直接使用self.step不断增加result，
            而是选择使用index变量，把self.begin与self.step和index的乘积相加，
            计算result的各个值，以此降低处理浮点数时累积效应致错的风险。
            """
            result = self.begin + self.step * idx


if __name__ == '__main__':
    ap = ArithmeticProgression(1, 1.32, 10)
    print(list(ap))

    ap2 = aritprog_gen(1, 1.32, 10)
    print(list(ap2))
