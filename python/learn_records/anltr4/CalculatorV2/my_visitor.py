if "." in __name__:
    from .CalculatorParser import CalculatorParser
    from .CalculatorVisitor import CalculatorVisitor
else:
    from CalculatorParser import CalculatorParser
    from CalculatorVisitor import CalculatorVisitor

import operator


class MyVisitor(CalculatorVisitor):
    def visitMulDiv(self, ctx: CalculatorParser.MulDivContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))

        if ctx.op.type == CalculatorParser.MUL:
            return operator.mul(left, right)
        else:
            return operator.truediv(left, right)

    def visitAddSub(self, ctx: CalculatorParser.AddSubContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))

        if ctx.op.type == CalculatorParser.Add:
            return operator.add(left, right)
        else:
            return operator.sub(left, right)

    def visitNum(self, ctx: CalculatorParser.NumContext):
        num_value = ctx.number().getText()
        if '.' in num_value:
            return float(num_value)
        else:
            return int(num_value)

    def visitParens(self, ctx: CalculatorParser.ParensContext):
        self.visit(ctx.expr())
