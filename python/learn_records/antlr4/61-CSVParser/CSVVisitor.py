# Generated from CSV.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CSVParser import CSVParser
else:
    from CSVParser import CSVParser

# This class defines a complete generic visitor for a parse tree produced by CSVParser.

class CSVVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CSVParser#rows.
    def visitRows(self, ctx:CSVParser.RowsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CSVParser#hdr.
    def visitHdr(self, ctx:CSVParser.HdrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CSVParser#row.
    def visitRow(self, ctx:CSVParser.RowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CSVParser#field.
    def visitField(self, ctx:CSVParser.FieldContext):
        return self.visitChildren(ctx)



del CSVParser