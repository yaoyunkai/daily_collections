# Generated from ./LExpr.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .LExprParser import LExprParser
else:
    from LExprParser import LExprParser

# This class defines a complete listener for a parse tree produced by LExprParser.
class LExprListener(ParseTreeListener):

    # Enter a parse tree produced by LExprParser#s.
    def enterS(self, ctx:LExprParser.SContext):
        pass

    # Exit a parse tree produced by LExprParser#s.
    def exitS(self, ctx:LExprParser.SContext):
        pass


    # Enter a parse tree produced by LExprParser#Add.
    def enterAdd(self, ctx:LExprParser.AddContext):
        pass

    # Exit a parse tree produced by LExprParser#Add.
    def exitAdd(self, ctx:LExprParser.AddContext):
        pass


    # Enter a parse tree produced by LExprParser#Mult.
    def enterMult(self, ctx:LExprParser.MultContext):
        pass

    # Exit a parse tree produced by LExprParser#Mult.
    def exitMult(self, ctx:LExprParser.MultContext):
        pass


    # Enter a parse tree produced by LExprParser#Int.
    def enterInt(self, ctx:LExprParser.IntContext):
        pass

    # Exit a parse tree produced by LExprParser#Int.
    def exitInt(self, ctx:LExprParser.IntContext):
        pass



del LExprParser