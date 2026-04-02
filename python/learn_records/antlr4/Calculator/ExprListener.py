# Generated from Expr.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ExprParser import ExprParser
else:
    from ExprParser import ExprParser

# This class defines a complete listener for a parse tree produced by ExprParser.
class ExprListener(ParseTreeListener):

    # Enter a parse tree produced by ExprParser#prog.
    def enterProg(self, ctx:ExprParser.ProgContext):
        pass

    # Exit a parse tree produced by ExprParser#prog.
    def exitProg(self, ctx:ExprParser.ProgContext):
        pass


    # Enter a parse tree produced by ExprParser#MulDivMod.
    def enterMulDivMod(self, ctx:ExprParser.MulDivModContext):
        pass

    # Exit a parse tree produced by ExprParser#MulDivMod.
    def exitMulDivMod(self, ctx:ExprParser.MulDivModContext):
        pass


    # Enter a parse tree produced by ExprParser#Number.
    def enterNumber(self, ctx:ExprParser.NumberContext):
        pass

    # Exit a parse tree produced by ExprParser#Number.
    def exitNumber(self, ctx:ExprParser.NumberContext):
        pass


    # Enter a parse tree produced by ExprParser#AddSub.
    def enterAddSub(self, ctx:ExprParser.AddSubContext):
        pass

    # Exit a parse tree produced by ExprParser#AddSub.
    def exitAddSub(self, ctx:ExprParser.AddSubContext):
        pass


    # Enter a parse tree produced by ExprParser#Percent.
    def enterPercent(self, ctx:ExprParser.PercentContext):
        pass

    # Exit a parse tree produced by ExprParser#Percent.
    def exitPercent(self, ctx:ExprParser.PercentContext):
        pass


    # Enter a parse tree produced by ExprParser#Parens.
    def enterParens(self, ctx:ExprParser.ParensContext):
        pass

    # Exit a parse tree produced by ExprParser#Parens.
    def exitParens(self, ctx:ExprParser.ParensContext):
        pass


    # Enter a parse tree produced by ExprParser#Pow.
    def enterPow(self, ctx:ExprParser.PowContext):
        pass

    # Exit a parse tree produced by ExprParser#Pow.
    def exitPow(self, ctx:ExprParser.PowContext):
        pass


    # Enter a parse tree produced by ExprParser#Unary.
    def enterUnary(self, ctx:ExprParser.UnaryContext):
        pass

    # Exit a parse tree produced by ExprParser#Unary.
    def exitUnary(self, ctx:ExprParser.UnaryContext):
        pass



del ExprParser