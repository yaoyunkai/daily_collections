# Generated from PropertyFile.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PropertyFileParser import PropertyFileParser
else:
    from PropertyFileParser import PropertyFileParser

# This class defines a complete listener for a parse tree produced by PropertyFileParser.
class PropertyFileListener(ParseTreeListener):

    # Enter a parse tree produced by PropertyFileParser#file.
    def enterFile(self, ctx:PropertyFileParser.FileContext):
        pass

    # Exit a parse tree produced by PropertyFileParser#file.
    def exitFile(self, ctx:PropertyFileParser.FileContext):
        pass


    # Enter a parse tree produced by PropertyFileParser#prop.
    def enterProp(self, ctx:PropertyFileParser.PropContext):
        pass

    # Exit a parse tree produced by PropertyFileParser#prop.
    def exitProp(self, ctx:PropertyFileParser.PropContext):
        pass



del PropertyFileParser