# Generated from C:/code/Py311/daily_collections/python/learn_records/anltr4/CalculatorV2/Calculator.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CalculatorParser import CalculatorParser
else:
    from CalculatorParser import CalculatorParser

# This class defines a complete generic visitor for a parse tree produced by CalculatorParser.

class CalculatorVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CalculatorParser#parens.
    def visitParens(self, ctx:CalculatorParser.ParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalculatorParser#MulDiv.
    def visitMulDiv(self, ctx:CalculatorParser.MulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalculatorParser#AddSub.
    def visitAddSub(self, ctx:CalculatorParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalculatorParser#num.
    def visitNum(self, ctx:CalculatorParser.NumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalculatorParser#number.
    def visitNumber(self, ctx:CalculatorParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CalculatorParser#decimal.
    def visitDecimal(self, ctx:CalculatorParser.DecimalContext):
        return self.visitChildren(ctx)



del CalculatorParser