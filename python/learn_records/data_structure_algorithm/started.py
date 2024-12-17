"""

异序词检测

created at 2024/12/17
"""
from collections import defaultdict


def anagram_sol(s1: str, s2: str):
    """
    拿第一个单词在第二个变量中寻找，找到后置为None


    """
    s2_list = list(s2)

    pos1 = 0
    still_ok = True

    while pos1 < len(s1) and still_ok:
        pos2 = 0
        found = False

        while pos2 < len(s2_list) and not found:
            if s1[pos1] == s2_list[pos2]:
                found = True
            else:
                pos2 += 1

        if found:
            s2_list[pos2] = None
        else:
            still_ok = False

        pos1 += 1

    return still_ok


def anagram_sol2(s1: str, s2: str):
    s1_list = list(s1)
    s2_list = list(s2)

    s1_list.sort()
    s2_list.sort()

    pos = 0
    matched = True

    while pos < len(s1) and matched:
        if s1_list[pos] == s2_list[pos]:
            pos += 1
        else:
            matched = False

    return matched


def anagram_sol3(s1: str, s2: str):
    cnt1 = defaultdict(int)
    cnt2 = defaultdict(int)

    for i in s1:
        cnt1[i] += 1
    for i in s2:
        cnt2[i] += 1

    return cnt1 == cnt2


if __name__ == '__main__':
    res1 = anagram_sol3('654', '456')
    print(res1)
