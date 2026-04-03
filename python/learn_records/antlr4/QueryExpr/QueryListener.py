# Generated from Query.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .QueryParser import QueryParser
else:
    from QueryParser import QueryParser

# This class defines a complete listener for a parse tree produced by QueryParser.
class QueryListener(ParseTreeListener):

    # Enter a parse tree produced by QueryParser#query.
    def enterQuery(self, ctx:QueryParser.QueryContext):
        pass

    # Exit a parse tree produced by QueryParser#query.
    def exitQuery(self, ctx:QueryParser.QueryContext):
        pass


    # Enter a parse tree produced by QueryParser#item.
    def enterItem(self, ctx:QueryParser.ItemContext):
        pass

    # Exit a parse tree produced by QueryParser#item.
    def exitItem(self, ctx:QueryParser.ItemContext):
        pass



del QueryParser