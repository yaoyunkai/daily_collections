"""


created at 2025/5/7
"""
from antlr4 import CommonTokenStream, InputStream

import HelloLexer
import HelloParser


def run_hello(expr: str):
    lexer = HelloLexer.HelloLexer(InputStream(expr))
    tokens = CommonTokenStream(lexer)
    parser = HelloParser.HelloParser(tokens)

    tree = parser.s()
    print(tree.toStringTree(recog=parser))


if __name__ == '__main__':
    run_hello('hello abcd')
