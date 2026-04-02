if "." in __name__:
    from .CalculatorParser import CalculatorParser
    from .CalculatorListener import CalculatorListener
else:
    from CalculatorParser import CalculatorParser
    from CalculatorListener import CalculatorListener

import operator


class MyListener(CalculatorListener):
    def __init__(self):
        self._stack = list()

    def get_result(self):
        return self._stack.pop()

    def exitMulDiv(self, ctx: CalculatorParser.MulDivContext):
        # super().exitMulDiv(ctx)
        right = self._stack.pop()
        left = self._stack.pop()
        if ctx.op.type == CalculatorParser.MUL:
            self._stack.append(operator.mul(left, right))
        else:
            self._stack.append(operator.truediv(left, right))

    def exitAddSub(self, ctx: CalculatorParser.AddSubContext):
        right = self._stack.pop()
        left = self._stack.pop()
        if ctx.op.type == CalculatorParser.Add:
            self._stack.append(operator.add(left, right))
        else:
            self._stack.append(operator.sub(left, right))

    def exitNum(self, ctx: CalculatorParser.NumContext):
        num_value = ctx.number().getText()
        if '.' in num_value:
            self._stack.append(float(num_value))
        else:
            self._stack.append(int(num_value))
