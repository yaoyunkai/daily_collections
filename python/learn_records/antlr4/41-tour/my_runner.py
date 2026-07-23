"""
my_runner.py


created at 2026-07-23
"""

from antlr4 import CommonTokenStream, InputStream

if "." in __name__:
    from .ExprLexer import ExprLexer
    from .ExprListener import ExprListener
    from .ExprParser import ExprParser
    from .LabeledExprLexer import LabeledExprLexer
    from .LabeledExprParser import LabeledExprParser
    from .LabeledExprVisitor import LabeledExprVisitor

else:
    from ExprLexer import ExprLexer
    from ExprListener import ExprListener
    from ExprParser import ExprParser
    from LabeledExprLexer import LabeledExprLexer
    from LabeledExprParser import LabeledExprParser
    from LabeledExprVisitor import LabeledExprVisitor


def get_expr_tree(value: str):
    _is = InputStream(value)
    lexer = ExprLexer(_is)
    tokens = CommonTokenStream(lexer)

    parser = ExprParser(tokens)
    tree = parser.prog()
    print(tree.toStringTree(recog=parser))


class EvalVisitor(LabeledExprVisitor):
    def __init__(self):
        self.memory: dict[str, int] = {}

    # ID '=' expr NEWLINE
    def visitAssign(self, ctx: LabeledExprParser.AssignContext) -> int:
        id_name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.memory[id_name] = value
        return value

    # expr NEWLINE
    def visitPrintExpr(self, ctx: LabeledExprParser.PrintExprContext) -> int:
        value = self.visit(ctx.expr())
        print(value)
        return 0

    # INT
    def visitInt(self, ctx: LabeledExprParser.IntContext) -> int:
        return int(ctx.INT().getText())

    # ID
    def visitId(self, ctx: LabeledExprParser.IdContext) -> int:
        id_name = ctx.ID().getText()
        # 如果 id_name 存在则返回对应的值，否则返回默认值 0
        return self.memory.get(id_name, 0)

    # expr op=('*'|'/') expr
    def visitMulDiv(self, ctx: LabeledExprParser.MulDivContext) -> int:
        left = self.visit(ctx.expr(0))  # get value of left subexpression
        right = self.visit(ctx.expr(1))  # get value of right subexpression

        if ctx.op.type == LabeledExprParser.MUL:
            return left * right
        return left // right

    # expr op=('+'|'-') expr
    def visitAddSub(self, ctx: LabeledExprParser.AddSubContext) -> int:
        left = self.visit(ctx.expr(0))  # get value of left subexpression
        right = self.visit(ctx.expr(1))  # get value of right subexpression

        if ctx.op.type == LabeledExprParser.ADD:
            return left + right
        return left - right  # must be SUB

    # '(' expr ')'
    def visitParens(self, ctx: LabeledExprParser.ParensContext) -> int:
        return self.visit(ctx.expr())  # return child expr's value


def calc(value: str):
    _is = InputStream(value)
    lexer = LabeledExprLexer(_is)
    tokens = CommonTokenStream(lexer)
    parser = LabeledExprParser(tokens)
    tree = parser.prog()

    eval_obj = EvalVisitor()
    eval_obj.visit(tree)


if __name__ == "__main__":
    demo1 = "1+2\n"

    get_expr_tree(demo1)
    calc(demo1)
