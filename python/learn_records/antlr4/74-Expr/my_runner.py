"""
my_runner.py


created at 2026-07-30
"""


if "." in __name__:
    from .LExprLexer import LExprLexer
    from .LExprListener import LExprListener
    from .LExprParser import LExprParser
    from .LExprVisitor import LExprVisitor
else:
    from LExprLexer import LExprLexer
    from LExprListener import LExprListener
    from LExprParser import LExprParser
    from LExprVisitor import LExprVisitor


class EvalVisitor(LExprVisitor):
    def visitMult(self, ctx: LExprParser.MultContext):
        return self.visit(ctx.e(0)) * self.visit(ctx.e(1))

    def visitAdd(self, ctx: LExprParser.AddContext):
        return self.visit(ctx.e(0)) + self.visit(ctx.e(1))

    def visitInt(self, ctx: LExprParser.IntContext):
        return int(ctx.INT().getText())


class EvalListener(LExprListener):
    def __init__(self):
        self.stack = []

    def exitMult(self, ctx: LExprParser.MultContext):
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(left * right)

    def exitAdd(self, ctx: LExprParser.AddContext):
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(left * right)

    def exitInt(self, ctx: LExprParser.IntContext):
        self.stack.append(int(ctx.INT().getText()))


class EvaluatorWithProps(LExprListener):
    pass
