from antlr4 import InputStream
from antlr4 import CommonTokenStream

if "." in __name__:
    from .CalculatorLexer import CalculatorLexer
    from .CalculatorParser import CalculatorParser
    from .my_visitor import MyVisitor
else:
    from CalculatorLexer import CalculatorLexer
    from CalculatorParser import CalculatorParser
    from my_visitor import MyVisitor


def calculate(expr: str):
    lexer = CalculatorLexer(InputStream(expr))
    tokens = CommonTokenStream(lexer)
    parser = CalculatorParser(tokens)

    tree = parser.expr()
    eval_visitor = MyVisitor()
    return eval_visitor.visit(tree)


if __name__ == '__main__':
    res = calculate('1+2*3+1.5')
    print(res)
