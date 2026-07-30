# Generated from ./CSV2.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,5,33,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,1,0,1,0,1,
        1,1,1,1,2,1,2,1,3,4,3,19,8,3,11,3,12,3,20,1,4,1,4,1,4,1,4,5,4,27,
        8,4,10,4,12,4,30,9,4,1,4,1,4,0,0,5,1,1,3,2,5,3,7,4,9,5,1,0,2,4,0,
        10,10,13,13,34,34,44,44,1,0,34,34,35,0,1,1,0,0,0,0,3,1,0,0,0,0,5,
        1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,1,11,1,0,0,0,3,13,1,0,0,0,5,15,1,
        0,0,0,7,18,1,0,0,0,9,22,1,0,0,0,11,12,5,44,0,0,12,2,1,0,0,0,13,14,
        5,13,0,0,14,4,1,0,0,0,15,16,5,10,0,0,16,6,1,0,0,0,17,19,8,0,0,0,
        18,17,1,0,0,0,19,20,1,0,0,0,20,18,1,0,0,0,20,21,1,0,0,0,21,8,1,0,
        0,0,22,28,5,34,0,0,23,24,5,34,0,0,24,27,5,34,0,0,25,27,8,1,0,0,26,
        23,1,0,0,0,26,25,1,0,0,0,27,30,1,0,0,0,28,26,1,0,0,0,28,29,1,0,0,
        0,29,31,1,0,0,0,30,28,1,0,0,0,31,32,5,34,0,0,32,10,1,0,0,0,4,0,20,
        26,28,0
    ]

class CSV2Lexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    TEXT = 4
    STRING = 5

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "','", "'\\r'", "'\\n'" ]

    symbolicNames = [ "<INVALID>",
            "TEXT", "STRING" ]

    ruleNames = [ "T__0", "T__1", "T__2", "TEXT", "STRING" ]

    grammarFileName = "CSV2.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


