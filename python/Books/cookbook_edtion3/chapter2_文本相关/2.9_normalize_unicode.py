"""

标准化Unicode

normalize:
    NFC  字符应该是整体组成
    NFD  表示字符应该分解为多个组合字符表示

    NFKC
    NFKD


Create at 2023/3/26 22:19
"""
import unicodedata


def test1():
    # 在Unicode中，某些字符能够用多个合法的编码表示

    # 在需要比较字符串的程序中使用字符的多种表示会产生问题。
    s1 = 'Spicy Jalape\u00f1o'  # 整体字符 ñ
    s2 = 'Spicy Jalapen\u0303o'  # 组合字符: 用拉丁字母”n”后面跟一个”~”的组合字符(U+0303)。
    print(s1.encode('utf8'))
    print(s2.encode('utf8'))

    t1 = unicodedata.normalize('NFC', s1)
    t2 = unicodedata.normalize('NFC', s2)

    print(t1.encode('utf8'))
    print(t2.encode('utf8'))


if __name__ == '__main__':
    test1()
