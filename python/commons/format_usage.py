"""
Format
https://docs.python.org/zh-cn/3.11/library/string.html#format-string-syntax

format_spec     ::=  [[fill]align][sign][z][#][0][width][grouping_option][.precision][type]
fill            ::=  <any character>
align           ::=  "<" | ">" | "=" | "^"
sign            ::=  "+" | "-" | " "
width           ::=  digit+
grouping_option ::=  "_" | ","
precision       ::=  digit+
type            ::=  "b" | "c" | "d" | "e" | "E" | "f" | "F" | "g" | "G" | "n" | "o" | "s" | "x" | "X" | "%"



为了将整数转换为二进制、八进制或十六进制的文本串， 可以分别使用
bin
oct
hex



Created at 2023/3/27
"""

ret1 = "repr() shows quotes: {0!r}; str() doesn't: {1!s}".format('test1', 'test2')
print(ret1)
