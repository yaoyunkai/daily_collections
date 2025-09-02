"""
匹配中文

Unicode 是一种字符集，而 UTF-8 是一种基于 Unicode 的可变长度字符编码。

1 字节：ASCII 字符，范围从 0x00 到 0x7F，也就是 Unicode 范围内的 U+0000 到 U+007F。
       0XXX XXXX
       127

2 字节：从 0x80 到 0x7FF，也就是 Unicode 范围内的 U+0080 到 U+07FF。
       110X XXXX 10XX XXXX
       2047

3 字节：从 0x800 到 0xFFFF，也就是 Unicode 范围内的 U+0800 到 U+FFFF。
       1110 XXXX 10XX XXXX 10XX XXXX
       65535

4 字节：从 0x10000 到 0x10FFFF，也就是 Unicode 范围内的 U+10000 到 U+10FFFF。
       1111 0XXX 10XX XXXX 10XX XXXX 10XX XXXX
       2097151


简体中文字符的编码范围：

GB 2312： 包括U+4E00到U+9FFF之间的汉字，以及U+E7C7到U+E7F3之间的次常用汉字和U+8140到U+81FE之间的符号等。
GBK：     在GB 2312的基础上扩展了更多的汉字和符号，包括U+A140到U+A3BF之间的部首、U+8140到U+A0FE之间的符号等。
GB 18030：在GBK的基础上进一步扩展了更多的汉字和符号，包括U+10000到U+2FA1D之间的汉字和U+0080到U+FFFD之间的其他字符。

繁体中文字符的编码范围：

Big5：包括U+4E00到U+9FFF之间的汉字、U+4B00到U+4BFB之间的部首和U+A140到U+A3BF之间的次常用汉字等。
Big5+：在Big5的基础上扩展了更多的汉字和符号，包括U+20000到U+2A6D6之间的汉字。

---------------------------------------------------
收到bytes类型时，先guess 是什么编码


Created at 2023/3/27
"""

import re

# gbk: C4E3BAC3 CAC0BDE7
text = "Hello 你好 World 世界"

demo2 = int('C4E3BAC3CAC0BDE7', 16).to_bytes(8, 'big', signed=False)
text2 = demo2.decode('gbk')

pattern = re.compile("[\u4e00-\u9fff\ue7c7-\ue7f3\u8140-\u81fe]+")  # 或者 pattern = re.compile("\p{Han}")
match = pattern.search(text2)

if match:
    print("匹配到汉字：", match.group())
else:
    print("没有匹配到汉字。")


def delta(a, b):
    res = int(b, 2) - int(a, 2)
    print(res)


if __name__ == '__main__':
    delta('0', '1111111')
    delta('0', '1' * 11)
    delta('0', '1' * 16)
    delta('0', '1' * 21)

    demo3 = '·！￥……（）—【】、；：“‘？。，《》'

    for i in demo3:
        print(i.encode('utf8'))
        print(hex(ord(i)))
