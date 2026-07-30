# Generated from ./CSV2.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CSV2Parser import CSV2Parser
else:
    from CSV2Parser import CSV2Parser

# This class defines a complete listener for a parse tree produced by CSV2Parser.
class CSV2Listener(ParseTreeListener):

    # Enter a parse tree produced by CSV2Parser#file.
    def enterFile(self, ctx:CSV2Parser.FileContext):
        pass

    # Exit a parse tree produced by CSV2Parser#file.
    def exitFile(self, ctx:CSV2Parser.FileContext):
        pass


    # Enter a parse tree produced by CSV2Parser#hdr.
    def enterHdr(self, ctx:CSV2Parser.HdrContext):
        pass

    # Exit a parse tree produced by CSV2Parser#hdr.
    def exitHdr(self, ctx:CSV2Parser.HdrContext):
        pass


    # Enter a parse tree produced by CSV2Parser#row.
    def enterRow(self, ctx:CSV2Parser.RowContext):
        pass

    # Exit a parse tree produced by CSV2Parser#row.
    def exitRow(self, ctx:CSV2Parser.RowContext):
        pass


    # Enter a parse tree produced by CSV2Parser#text.
    def enterText(self, ctx:CSV2Parser.TextContext):
        pass

    # Exit a parse tree produced by CSV2Parser#text.
    def exitText(self, ctx:CSV2Parser.TextContext):
        pass


    # Enter a parse tree produced by CSV2Parser#string.
    def enterString(self, ctx:CSV2Parser.StringContext):
        pass

    # Exit a parse tree produced by CSV2Parser#string.
    def exitString(self, ctx:CSV2Parser.StringContext):
        pass


    # Enter a parse tree produced by CSV2Parser#empty.
    def enterEmpty(self, ctx:CSV2Parser.EmptyContext):
        pass

    # Exit a parse tree produced by CSV2Parser#empty.
    def exitEmpty(self, ctx:CSV2Parser.EmptyContext):
        pass



del CSV2Parser