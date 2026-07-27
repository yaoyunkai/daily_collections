# Generated from CSV.g4 by ANTLR 4.13.2
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

class CSVParser ( Parser ):

    grammarFileName = "CSV.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "','", "'\\r'", "'\\n'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "TEXT", "STRING" ]

    RULE_rows = 0
    RULE_hdr = 1
    RULE_row = 2
    RULE_field = 3

    ruleNames =  [ "rows", "hdr", "row", "field" ]

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




    class RowsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def hdr(self):
            return self.getTypedRuleContext(CSVParser.HdrContext,0)


        def row(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CSVParser.RowContext)
            else:
                return self.getTypedRuleContext(CSVParser.RowContext,i)


        def getRuleIndex(self):
            return CSVParser.RULE_rows

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRows" ):
                listener.enterRows(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRows" ):
                listener.exitRows(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRows" ):
                return visitor.visitRows(self)
            else:
                return visitor.visitChildren(self)




    def rows(self):

        localctx = CSVParser.RowsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_rows)
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
            return self.getTypedRuleContext(CSVParser.RowContext,0)


        def getRuleIndex(self):
            return CSVParser.RULE_hdr

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

        localctx = CSVParser.HdrContext(self, self._ctx, self.state)
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
                return self.getTypedRuleContexts(CSVParser.FieldContext)
            else:
                return self.getTypedRuleContext(CSVParser.FieldContext,i)


        def getRuleIndex(self):
            return CSVParser.RULE_row

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

        localctx = CSVParser.RowContext(self, self._ctx, self.state)
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
                self.match(CSVParser.T__0)
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
                self.match(CSVParser.T__1)


            self.state = 27
            self.match(CSVParser.T__2)
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

        def TEXT(self):
            return self.getToken(CSVParser.TEXT, 0)

        def STRING(self):
            return self.getToken(CSVParser.STRING, 0)

        def getRuleIndex(self):
            return CSVParser.RULE_field

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterField" ):
                listener.enterField(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitField" ):
                listener.exitField(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitField" ):
                return visitor.visitField(self)
            else:
                return visitor.visitChildren(self)




    def field(self):

        localctx = CSVParser.FieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_field)
        try:
            self.state = 32
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 29
                self.match(CSVParser.TEXT)
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 2)
                self.state = 30
                self.match(CSVParser.STRING)
                pass
            elif token in [1, 2, 3]:
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





