# Generated from PropertyFile.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,4,27,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,1,0,1,1,1,1,1,
        2,4,2,15,8,2,11,2,12,2,16,1,3,1,3,5,3,21,8,3,10,3,12,3,24,9,3,1,
        3,1,3,1,22,0,4,1,1,3,2,5,3,7,4,1,0,1,1,0,97,122,28,0,1,1,0,0,0,0,
        3,1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,1,9,1,0,0,0,3,11,1,0,0,0,5,14,
        1,0,0,0,7,18,1,0,0,0,9,10,5,61,0,0,10,2,1,0,0,0,11,12,5,10,0,0,12,
        4,1,0,0,0,13,15,7,0,0,0,14,13,1,0,0,0,15,16,1,0,0,0,16,14,1,0,0,
        0,16,17,1,0,0,0,17,6,1,0,0,0,18,22,5,34,0,0,19,21,9,0,0,0,20,19,
        1,0,0,0,21,24,1,0,0,0,22,23,1,0,0,0,22,20,1,0,0,0,23,25,1,0,0,0,
        24,22,1,0,0,0,25,26,5,34,0,0,26,8,1,0,0,0,3,0,16,22,0
    ]

class PropertyFileLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    ID = 3
    STRING = 4

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'='", "'\\n'" ]

    symbolicNames = [ "<INVALID>",
            "ID", "STRING" ]

    ruleNames = [ "T__0", "T__1", "ID", "STRING" ]

    grammarFileName = "PropertyFile.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


