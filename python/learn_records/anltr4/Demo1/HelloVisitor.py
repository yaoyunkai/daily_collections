# Generated from D:/Code/python/daily_collections/python/learn_records/anltr4/Demo1/Hello.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .HelloParser import HelloParser
else:
    from HelloParser import HelloParser

# This class defines a complete generic visitor for a parse tree produced by HelloParser.

class HelloVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by HelloParser#s.
    def visitS(self, ctx:HelloParser.SContext):
        return self.visitChildren(ctx)



del HelloParser