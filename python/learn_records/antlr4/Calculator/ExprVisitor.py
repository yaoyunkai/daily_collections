# Generated from Expr.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .ExprParser import ExprParser
else:
    from ExprParser import ExprParser

# This class defines a complete generic visitor for a parse tree produced by ExprParser.

class ExprVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ExprParser#prog.
    def visitProg(self, ctx:ExprParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#MulDivMod.
    def visitMulDivMod(self, ctx:ExprParser.MulDivModContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#Number.
    def visitNumber(self, ctx:ExprParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#AddSub.
    def visitAddSub(self, ctx:ExprParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#Percent.
    def visitPercent(self, ctx:ExprParser.PercentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#Parens.
    def visitParens(self, ctx:ExprParser.ParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#Pow.
    def visitPow(self, ctx:ExprParser.PowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#Unary.
    def visitUnary(self, ctx:ExprParser.UnaryContext):
        return self.visitChildren(ctx)



del ExprParser