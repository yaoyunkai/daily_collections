# Generated from CSV.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CSVParser import CSVParser
else:
    from CSVParser import CSVParser

# This class defines a complete listener for a parse tree produced by CSVParser.
class CSVListener(ParseTreeListener):

    # Enter a parse tree produced by CSVParser#rows.
    def enterRows(self, ctx:CSVParser.RowsContext):
        pass

    # Exit a parse tree produced by CSVParser#rows.
    def exitRows(self, ctx:CSVParser.RowsContext):
        pass


    # Enter a parse tree produced by CSVParser#hdr.
    def enterHdr(self, ctx:CSVParser.HdrContext):
        pass

    # Exit a parse tree produced by CSVParser#hdr.
    def exitHdr(self, ctx:CSVParser.HdrContext):
        pass


    # Enter a parse tree produced by CSVParser#row.
    def enterRow(self, ctx:CSVParser.RowContext):
        pass

    # Exit a parse tree produced by CSVParser#row.
    def exitRow(self, ctx:CSVParser.RowContext):
        pass


    # Enter a parse tree produced by CSVParser#field.
    def enterField(self, ctx:CSVParser.FieldContext):
        pass

    # Exit a parse tree produced by CSVParser#field.
    def exitField(self, ctx:CSVParser.FieldContext):
        pass



del CSVParser