# Generated from Query.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,3,21,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,1,0,4,0,9,8,0,11,0,12,0,10,
        1,1,4,1,14,8,1,11,1,12,1,15,1,1,1,1,1,2,1,2,0,0,3,1,1,3,2,5,3,1,
        0,2,7,0,37,37,43,43,45,57,61,61,65,90,95,95,97,122,5,0,9,10,13,13,
        32,32,44,44,59,59,22,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,1,8,1,0,
        0,0,3,13,1,0,0,0,5,19,1,0,0,0,7,9,7,0,0,0,8,7,1,0,0,0,9,10,1,0,0,
        0,10,8,1,0,0,0,10,11,1,0,0,0,11,2,1,0,0,0,12,14,7,1,0,0,13,12,1,
        0,0,0,14,15,1,0,0,0,15,13,1,0,0,0,15,16,1,0,0,0,16,17,1,0,0,0,17,
        18,6,1,0,0,18,4,1,0,0,0,19,20,9,0,0,0,20,6,1,0,0,0,3,0,10,15,1,6,
        0,0
    ]

class QueryLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    WORD = 1
    SEP = 2
    ERR = 3

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
 ]

    symbolicNames = [ "<INVALID>",
            "WORD", "SEP", "ERR" ]

    ruleNames = [ "WORD", "SEP", "ERR" ]

    grammarFileName = "Query.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


