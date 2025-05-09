from antlr4 import CommonTokenStream
from antlr4 import InputStream
from antlr4 import ParseTreeWalker

if "." in __name__:
    from .CalculatorLexer import CalculatorLexer
    from .CalculatorParser import CalculatorParser
    from .my_visitor import MyVisitor
    from .my_listener import MyListener
else:
    from CalculatorLexer import CalculatorLexer
    from CalculatorParser import CalculatorParser
    from my_visitor import MyVisitor
    from my_listener import MyListener


def calculate(expr: str):
    lexer = CalculatorLexer(InputStream(expr))
    tokens = CommonTokenStream(lexer)
    parser = CalculatorParser(tokens)

    tree = parser.expr()
    eval_visitor = MyVisitor()
    return eval_visitor.visit(tree)


def calculate_with_listener(expr: str):
    lexer = CalculatorLexer(InputStream(expr))
    tokens = CommonTokenStream(lexer)
    parser = CalculatorParser(tokens)

    tree = parser.expr()
    walker = ParseTreeWalker()
    listener = MyListener()

    walker.walk(listener, tree)
    return listener.get_result()


if __name__ == '__main__':
    # res = calculate('1+2*3+1.5')
    res = calculate_with_listener('1+2*3+1.5')
    print(res)
