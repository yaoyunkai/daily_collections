# Generated from ArrayInit.g4 by ANTLR 4.13.2
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
        4,1,5,20,2,0,7,0,2,1,7,1,1,0,1,0,1,0,1,0,5,0,9,8,0,10,0,12,0,12,
        9,0,1,0,1,0,1,1,1,1,3,1,18,8,1,1,1,0,0,2,0,2,0,0,19,0,4,1,0,0,0,
        2,17,1,0,0,0,4,5,5,1,0,0,5,10,3,2,1,0,6,7,5,2,0,0,7,9,3,2,1,0,8,
        6,1,0,0,0,9,12,1,0,0,0,10,8,1,0,0,0,10,11,1,0,0,0,11,13,1,0,0,0,
        12,10,1,0,0,0,13,14,5,3,0,0,14,1,1,0,0,0,15,18,3,0,0,0,16,18,5,4,
        0,0,17,15,1,0,0,0,17,16,1,0,0,0,18,3,1,0,0,0,2,10,17
    ]

class ArrayInitParser ( Parser ):

    grammarFileName = "ArrayInit.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'{'", "','", "'}'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "INT", "WS" ]

    RULE_init = 0
    RULE_value = 1

    ruleNames =  [ "init", "value" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    INT=4
    WS=5

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class InitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def value(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ArrayInitParser.ValueContext)
            else:
                return self.getTypedRuleContext(ArrayInitParser.ValueContext,i)


        def getRuleIndex(self):
            return ArrayInitParser.RULE_init

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInit" ):
                listener.enterInit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInit" ):
                listener.exitInit(self)




    def init(self):

        localctx = ArrayInitParser.InitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_init)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 4
            self.match(ArrayInitParser.T__0)
            self.state = 5
            self.value()
            self.state = 10
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==2:
                self.state = 6
                self.match(ArrayInitParser.T__1)
                self.state = 7
                self.value()
                self.state = 12
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 13
            self.match(ArrayInitParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def init(self):
            return self.getTypedRuleContext(ArrayInitParser.InitContext,0)


        def INT(self):
            return self.getToken(ArrayInitParser.INT, 0)

        def getRuleIndex(self):
            return ArrayInitParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)




    def value(self):

        localctx = ArrayInitParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_value)
        try:
            self.state = 17
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 15
                self.init()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 16
                self.match(ArrayInitParser.INT)
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





