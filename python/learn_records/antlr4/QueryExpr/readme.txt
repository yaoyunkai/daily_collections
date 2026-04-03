一个查询框传入的字符处理。己经准备好了antlr4的相关环境，请使用python实现代码.

1, 忽略空白字符
2, ; ,  用来分隔单词, 未连起来的单词 比如 ABC DEF 也当作 ["ABC", "DEF"],
3, % _ 表示模式匹配。
4, 正常的词是这样的 0-9 a-z A-Z 和 "+ / = - ."，但是不能全是"+ / = - ." 而没有0-9和a-z A-Z
5, 模式匹配的词也是一样，0-9 a-z A-Z 和 "+ / = - ." _  % , 但不能全是  "+ / = - ." _ %

以下是一些例子:

ABC -> [('N', "ABC"),]
ABC_ -> [('P', "ABC_"),]
ABC% -> [('P', "ABC%"),]

" ABCD   " -> [('N', "ABCD"),]

ABCD;ABC -> [('N', 'ABCD'), ('N', "ABC")]

ABCD,BCD% -> [('N', 'ABCD'), ('P', 'BCD%')]

ABC DEF-SDF  -> [('N', "ABC"), ('N', "DEF-SDF")]

ABC \n CDF  -> [('N', 'ABC'), ('N', 'CDF')]

"         " -> invalid, return [] or raise error ?, should return []

"    +++++" -> invalid

"+++++%%%%%, ABCD" -> [("N", 'ABCD')]
