# Generated from LabeledExpr.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .LabeledExprParser import LabeledExprParser
else:
    from LabeledExprParser import LabeledExprParser

# This class defines a complete listener for a parse tree produced by LabeledExprParser.
class LabeledExprListener(ParseTreeListener):

    # Enter a parse tree produced by LabeledExprParser#prog.
    def enterProg(self, ctx:LabeledExprParser.ProgContext):
        pass

    # Exit a parse tree produced by LabeledExprParser#prog.
    def exitProg(self, ctx:LabeledExprParser.ProgContext):
        pass


    # Enter a parse tree produced by LabeledExprParser#printExpr.
    def enterPrintExpr(self, ctx:LabeledExprParser.PrintExprContext):
        pass

    # Exit a parse tree produced by LabeledExprParser#printExpr.
    def exitPrintExpr(self, ctx:LabeledExprParser.PrintExprContext):
        pass


    # Enter a parse tree produced by LabeledExprParser#assign.
    def enterAssign(self, ctx:LabeledExprParser.AssignContext):
        pass

    # Exit a parse tree produced by LabeledExprParser#assign.
    def exitAssign(self, ctx:LabeledExprParser.AssignContext):
        pass


    # Enter a parse tree produced by LabeledExprParser#blank.
    def enterBlank(self, ctx:LabeledExprParser.BlankContext):
        pass

    # Exit a parse tree produced by LabeledExprParser#blank.
    def exitBlank(self, ctx:LabeledExprParser.BlankContext):
        pass


    # Enter a parse tree produced by LabeledExprParser#parens.
    def enterParens(self, ctx:LabeledExprParser.ParensContext):
        pass

    # Exit a parse tree produced by LabeledExprParser#parens.
    def exitParens(self, ctx:LabeledExprParser.ParensContext):
        pass


    # Enter a parse tree produced by LabeledExprParser#MulDiv.
    def enterMulDiv(self, ctx:LabeledExprParser.MulDivContext):
        pass

    # Exit a parse tree produced by LabeledExprParser#MulDiv.
    def exitMulDiv(self, ctx:LabeledExprParser.MulDivContext):
        pass


    # Enter a parse tree produced by LabeledExprParser#AddSub.
    def enterAddSub(self, ctx:LabeledExprParser.AddSubContext):
        pass

    # Exit a parse tree produced by LabeledExprParser#AddSub.
    def exitAddSub(self, ctx:LabeledExprParser.AddSubContext):
        pass


    # Enter a parse tree produced by LabeledExprParser#id.
    def enterId(self, ctx:LabeledExprParser.IdContext):
        pass

    # Exit a parse tree produced by LabeledExprParser#id.
    def exitId(self, ctx:LabeledExprParser.IdContext):
        pass


    # Enter a parse tree produced by LabeledExprParser#int.
    def enterInt(self, ctx:LabeledExprParser.IntContext):
        pass

    # Exit a parse tree produced by LabeledExprParser#int.
    def exitInt(self, ctx:LabeledExprParser.IntContext):
        pass



del LabeledExprParser