# Generated from C:/code/Py311/daily_collections/python/learn_records/anltr4/CalculatorV2/Calculator.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,8,36,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,1,0,1,0,1,1,1,1,1,2,4,2,23,8,2,11,2,12,2,24,1,3,1,
        3,1,4,1,4,1,5,1,5,1,6,1,6,1,7,1,7,0,0,8,1,1,3,2,5,3,7,4,9,5,11,6,
        13,7,15,8,1,0,1,1,0,48,57,36,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,
        0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,1,
        17,1,0,0,0,3,19,1,0,0,0,5,22,1,0,0,0,7,26,1,0,0,0,9,28,1,0,0,0,11,
        30,1,0,0,0,13,32,1,0,0,0,15,34,1,0,0,0,17,18,5,40,0,0,18,2,1,0,0,
        0,19,20,5,41,0,0,20,4,1,0,0,0,21,23,7,0,0,0,22,21,1,0,0,0,23,24,
        1,0,0,0,24,22,1,0,0,0,24,25,1,0,0,0,25,6,1,0,0,0,26,27,5,46,0,0,
        27,8,1,0,0,0,28,29,5,42,0,0,29,10,1,0,0,0,30,31,5,47,0,0,31,12,1,
        0,0,0,32,33,5,43,0,0,33,14,1,0,0,0,34,35,5,45,0,0,35,16,1,0,0,0,
        2,0,24,0
    ]

class CalculatorLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    INT = 3
    DOT = 4
    MUL = 5
    DIV = 6
    Add = 7
    SUB = 8

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "')'", "'.'", "'*'", "'/'", "'+'", "'-'" ]

    symbolicNames = [ "<INVALID>",
            "INT", "DOT", "MUL", "DIV", "Add", "SUB" ]

    ruleNames = [ "T__0", "T__1", "INT", "DOT", "MUL", "DIV", "Add", "SUB" ]

    grammarFileName = "Calculator.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


