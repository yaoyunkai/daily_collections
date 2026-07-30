# Generated from PropertyFile.g4 by ANTLR 4.13.2
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
        4,1,4,15,2,0,7,0,2,1,7,1,1,0,4,0,6,8,0,11,0,12,0,7,1,1,1,1,1,1,1,
        1,1,1,1,1,0,0,2,0,2,0,0,13,0,5,1,0,0,0,2,9,1,0,0,0,4,6,3,2,1,0,5,
        4,1,0,0,0,6,7,1,0,0,0,7,5,1,0,0,0,7,8,1,0,0,0,8,1,1,0,0,0,9,10,5,
        3,0,0,10,11,5,1,0,0,11,12,5,4,0,0,12,13,5,2,0,0,13,3,1,0,0,0,1,7
    ]

class PropertyFileParser ( Parser ):

    grammarFileName = "PropertyFile.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'='", "'\\n'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "ID", "STRING" ]

    RULE_file = 0
    RULE_prop = 1

    ruleNames =  [ "file", "prop" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    ID=3
    STRING=4

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

        def prop(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PropertyFileParser.PropContext)
            else:
                return self.getTypedRuleContext(PropertyFileParser.PropContext,i)


        def getRuleIndex(self):
            return PropertyFileParser.RULE_file

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

        localctx = PropertyFileParser.FileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_file)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 5 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 4
                self.prop()
                self.state = 7 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==3):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PropContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(PropertyFileParser.ID, 0)

        def STRING(self):
            return self.getToken(PropertyFileParser.STRING, 0)

        def getRuleIndex(self):
            return PropertyFileParser.RULE_prop

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProp" ):
                listener.enterProp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProp" ):
                listener.exitProp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProp" ):
                return visitor.visitProp(self)
            else:
                return visitor.visitChildren(self)




    def prop(self):

        localctx = PropertyFileParser.PropContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_prop)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 9
            self.match(PropertyFileParser.ID)
            self.state = 10
            self.match(PropertyFileParser.T__0)
            self.state = 11
            self.match(PropertyFileParser.STRING)
            self.state = 12
            self.match(PropertyFileParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





