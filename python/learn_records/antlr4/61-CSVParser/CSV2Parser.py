# Generated from ./CSV2.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,5,35,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,1,0,4,0,11,8,0,11,0,
        12,0,12,1,1,1,1,1,2,1,2,1,2,5,2,20,8,2,10,2,12,2,23,9,2,1,2,3,2,
        26,8,2,1,2,1,2,1,3,1,3,1,3,3,3,33,8,3,1,3,0,0,4,0,2,4,6,0,0,35,0,
        8,1,0,0,0,2,14,1,0,0,0,4,16,1,0,0,0,6,32,1,0,0,0,8,10,3,2,1,0,9,
        11,3,4,2,0,10,9,1,0,0,0,11,12,1,0,0,0,12,10,1,0,0,0,12,13,1,0,0,
        0,13,1,1,0,0,0,14,15,3,4,2,0,15,3,1,0,0,0,16,21,3,6,3,0,17,18,5,
        1,0,0,18,20,3,6,3,0,19,17,1,0,0,0,20,23,1,0,0,0,21,19,1,0,0,0,21,
        22,1,0,0,0,22,25,1,0,0,0,23,21,1,0,0,0,24,26,5,2,0,0,25,24,1,0,0,
        0,25,26,1,0,0,0,26,27,1,0,0,0,27,28,5,3,0,0,28,5,1,0,0,0,29,33,5,
        4,0,0,30,33,5,5,0,0,31,33,1,0,0,0,32,29,1,0,0,0,32,30,1,0,0,0,32,
        31,1,0,0,0,33,7,1,0,0,0,4,12,21,25,32
    ]

class CSV2Parser ( Parser ):

    grammarFileName = "CSV2.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "','", "'\\r'", "'\\n'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "TEXT", "STRING" ]

    RULE_file = 0
    RULE_hdr = 1
    RULE_row = 2
    RULE_field = 3

    ruleNames =  [ "file", "hdr", "row", "field" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    TEXT=4
    STRING=5

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class FileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def hdr(self):
            return self.getTypedRuleContext(CSV2Parser.HdrContext,0)


        def row(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CSV2Parser.RowContext)
            else:
                return self.getTypedRuleContext(CSV2Parser.RowContext,i)


        def getRuleIndex(self):
            return CSV2Parser.RULE_file

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFile" ):
                listener.enterFile(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFile" ):
                listener.exitFile(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFile" ):
                return visitor.visitFile(self)
            else:
                return visitor.visitChildren(self)




    def file_(self):

        localctx = CSV2Parser.FileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_file)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 8
            self.hdr()
            self.state = 10 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 9
                self.row()
                self.state = 12 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 62) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class HdrContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def row(self):
            return self.getTypedRuleContext(CSV2Parser.RowContext,0)


        def getRuleIndex(self):
            return CSV2Parser.RULE_hdr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHdr" ):
                listener.enterHdr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHdr" ):
                listener.exitHdr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHdr" ):
                return visitor.visitHdr(self)
            else:
                return visitor.visitChildren(self)




    def hdr(self):

        localctx = CSV2Parser.HdrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_hdr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 14
            self.row()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RowContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def field(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CSV2Parser.FieldContext)
            else:
                return self.getTypedRuleContext(CSV2Parser.FieldContext,i)


        def getRuleIndex(self):
            return CSV2Parser.RULE_row

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRow" ):
                listener.enterRow(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRow" ):
                listener.exitRow(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRow" ):
                return visitor.visitRow(self)
            else:
                return visitor.visitChildren(self)




    def row(self):

        localctx = CSV2Parser.RowContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_row)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 16
            self.field()
            self.state = 21
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 17
                self.match(CSV2Parser.T__0)
                self.state = 18
                self.field()
                self.state = 23
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 25
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==2:
                self.state = 24
                self.match(CSV2Parser.T__1)


            self.state = 27
            self.match(CSV2Parser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FieldContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CSV2Parser.RULE_field

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class StringContext(FieldContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CSV2Parser.FieldContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(CSV2Parser.STRING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterString" ):
                listener.enterString(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitString" ):
                listener.exitString(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString" ):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)


    class TextContext(FieldContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CSV2Parser.FieldContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def TEXT(self):
            return self.getToken(CSV2Parser.TEXT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterText" ):
                listener.enterText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitText" ):
                listener.exitText(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitText" ):
                return visitor.visitText(self)
            else:
                return visitor.visitChildren(self)


    class EmptyContext(FieldContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CSV2Parser.FieldContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEmpty" ):
                listener.enterEmpty(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEmpty" ):
                listener.exitEmpty(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEmpty" ):
                return visitor.visitEmpty(self)
            else:
                return visitor.visitChildren(self)



    def field(self):

        localctx = CSV2Parser.FieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_field)
        try:
            self.state = 32
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                localctx = CSV2Parser.TextContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 29
                self.match(CSV2Parser.TEXT)
                pass
            elif token in [5]:
                localctx = CSV2Parser.StringContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 30
                self.match(CSV2Parser.STRING)
                pass
            elif token in [1, 2, 3]:
                localctx = CSV2Parser.EmptyContext(self, localctx)
                self.enterOuterAlt(localctx, 3)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





