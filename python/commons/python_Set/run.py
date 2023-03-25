"""

集合相关运算
    isdisjoint 如果集合中没有与 other 共有的元素则返回 True。
               当且仅当两个集合的交集为空集合时，两者为不相交集合。
    issubset:
        set <= other
        set <  other  真子集

    issuperset:
        set >= other  检测是否 other 中的每个元素都在集合之中。
        set >  other  真超集

    union(*others)
        set | other | ...   并集

    intersection(*others)
        set & other & ...   交集

    difference(*others)
        set - other - ...  差集

    symmetric_difference(other)
        set ^ other   返回一个新集合，其中的元素或属于原集合或属于 other 指定的其他集合，但不能同时属于两者。

use redis



Created at 2023/3/7
"""

a = {1, 2, 3, 4}
b = {2, 3, 4, 5}


def compute():
    t1 = a - b
    t2 = b - a

    t3 = a ^ b

    print(t1 | t2)
    print(t3)


if __name__ == '__main__':
    compute()
