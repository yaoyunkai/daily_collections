import sys

from antlr4 import *  # noqa: F403
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from ExprVisitor import ExprVisitor


class EvalVisitor(ExprVisitor):
    # 根节点
    def visitProg(self, ctx: ExprParser.ProgContext):
        return self.visit(ctx.expr())

    # 提取数字
    def visitNumber(self, ctx: ExprParser.NumberContext):
        return float(ctx.NUMBER().getText())

    # 处理括号 ()
    def visitParens(self, ctx: ExprParser.ParensContext):
        return self.visit(ctx.expr())

    # 处理百分比后缀 (例如 45%)
    def visitPercent(self, ctx: ExprParser.PercentContext):
        value = self.visit(ctx.expr())
        return value / 100.0

    # 处理指数 ^
    def visitPow(self, ctx: ExprParser.PowContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return left**right

    # 处理一元正负号 (例如 -3, +5)
    def visitUnary(self, ctx: ExprParser.UnaryContext):
        value = self.visit(ctx.expr())
        if ctx.op.type == ExprParser.MINUS:
            return -value
        return value

    # 处理乘、除、求余 (*, /, %)
    def visitMulDivMod(self, ctx: ExprParser.MulDivModContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))

        if ctx.op.type == ExprParser.MUL:
            return left * right
        elif ctx.op.type == ExprParser.DIV:
            if right == 0:
                raise ZeroDivisionError("除数不能为0")
            return left / right
        elif ctx.op.type == ExprParser.MOD:
            if right == 0:
                raise ZeroDivisionError("求余的底数不能为0")
            return left % right

    # 处理加、减 (+, -)
    def visitAddSub(self, ctx: ExprParser.AddSubContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))

        if ctx.op.type == ExprParser.PLUS:
            return left + right
        elif ctx.op.type == ExprParser.MINUS:
            return left - right


def evaluate_expression(expression: str):
    """封装解析与计算过程"""
    input_stream = InputStream(expression)
    lexer = ExprLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ExprParser(stream)

    # 解析入口为 prog
    tree = parser.prog()

    # 使用 Visitor 进行计算
    visitor = EvalVisitor()
    return visitor.visit(tree)


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        "2",
        "-3",
        "-19.03",
        "19.33",
        "-(5+4) + 5",  # 括号与一元负号
        "2^4",  # 指数
        "45%",  # 百分比
        "12.34%",  # 小数百分比
        "8%4",  # 整数求余
        "89.4%44.2",  # 小数求余
        "-67.45^4%",  # 综合：一元负号、小数、指数、百分比
        "2 * (3 + 5) % 3",  # 综合：优先级测试
        "34-45 *",
    ]

    print("=== 表达式计算结果 ===")
    for expr in test_cases:
        try:
            result = evaluate_expression(expr)
            print(f"{expr:<20} = {result}")
        except Exception as e:
            print(f"{expr:<20} = Error: {e}")
