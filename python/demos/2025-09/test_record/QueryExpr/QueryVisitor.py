# Generated from Query.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .QueryParser import QueryParser
else:
    from QueryParser import QueryParser

# This class defines a complete generic visitor for a parse tree produced by QueryParser.

class QueryVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by QueryParser#query.
    def visitQuery(self, ctx:QueryParser.QueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QueryParser#item.
    def visitItem(self, ctx:QueryParser.ItemContext):
        return self.visitChildren(ctx)



del QueryParser