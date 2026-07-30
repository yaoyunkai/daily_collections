# Generated from ./CSV2.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CSV2Parser import CSV2Parser
else:
    from CSV2Parser import CSV2Parser

# This class defines a complete generic visitor for a parse tree produced by CSV2Parser.

class CSV2Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by CSV2Parser#file.
    def visitFile(self, ctx:CSV2Parser.FileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CSV2Parser#hdr.
    def visitHdr(self, ctx:CSV2Parser.HdrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CSV2Parser#row.
    def visitRow(self, ctx:CSV2Parser.RowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CSV2Parser#text.
    def visitText(self, ctx:CSV2Parser.TextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CSV2Parser#string.
    def visitString(self, ctx:CSV2Parser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CSV2Parser#empty.
    def visitEmpty(self, ctx:CSV2Parser.EmptyContext):
        return self.visitChildren(ctx)



del CSV2Parser