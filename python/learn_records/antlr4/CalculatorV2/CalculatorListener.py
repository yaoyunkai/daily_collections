# Generated from C:/code/Py311/daily_collections/python/learn_records/anltr4/CalculatorV2/Calculator.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CalculatorParser import CalculatorParser
else:
    from CalculatorParser import CalculatorParser

# This class defines a complete listener for a parse tree produced by CalculatorParser.
class CalculatorListener(ParseTreeListener):

    # Enter a parse tree produced by CalculatorParser#parens.
    def enterParens(self, ctx:CalculatorParser.ParensContext):
        pass

    # Exit a parse tree produced by CalculatorParser#parens.
    def exitParens(self, ctx:CalculatorParser.ParensContext):
        pass


    # Enter a parse tree produced by CalculatorParser#MulDiv.
    def enterMulDiv(self, ctx:CalculatorParser.MulDivContext):
        pass

    # Exit a parse tree produced by CalculatorParser#MulDiv.
    def exitMulDiv(self, ctx:CalculatorParser.MulDivContext):
        pass


    # Enter a parse tree produced by CalculatorParser#AddSub.
    def enterAddSub(self, ctx:CalculatorParser.AddSubContext):
        pass

    # Exit a parse tree produced by CalculatorParser#AddSub.
    def exitAddSub(self, ctx:CalculatorParser.AddSubContext):
        pass


    # Enter a parse tree produced by CalculatorParser#num.
    def enterNum(self, ctx:CalculatorParser.NumContext):
        pass

    # Exit a parse tree produced by CalculatorParser#num.
    def exitNum(self, ctx:CalculatorParser.NumContext):
        pass


    # Enter a parse tree produced by CalculatorParser#number.
    def enterNumber(self, ctx:CalculatorParser.NumberContext):
        pass

    # Exit a parse tree produced by CalculatorParser#number.
    def exitNumber(self, ctx:CalculatorParser.NumberContext):
        pass


    # Enter a parse tree produced by CalculatorParser#decimal.
    def enterDecimal(self, ctx:CalculatorParser.DecimalContext):
        pass

    # Exit a parse tree produced by CalculatorParser#decimal.
    def exitDecimal(self, ctx:CalculatorParser.DecimalContext):
        pass



del CalculatorParser