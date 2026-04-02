# Generated from Expr.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,10,57,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,
        4,1,4,1,5,1,5,1,6,1,6,1,7,1,7,1,8,4,8,39,8,8,11,8,12,8,40,1,8,1,
        8,4,8,45,8,8,11,8,12,8,46,3,8,49,8,8,1,9,4,9,52,8,9,11,9,12,9,53,
        1,9,1,9,0,0,10,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,1,0,
        2,1,0,48,57,3,0,9,10,13,13,32,32,60,0,1,1,0,0,0,0,3,1,0,0,0,0,5,
        1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,
        0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,1,21,1,0,0,0,3,23,1,0,0,0,5,25,1,
        0,0,0,7,27,1,0,0,0,9,29,1,0,0,0,11,31,1,0,0,0,13,33,1,0,0,0,15,35,
        1,0,0,0,17,38,1,0,0,0,19,51,1,0,0,0,21,22,5,43,0,0,22,2,1,0,0,0,
        23,24,5,45,0,0,24,4,1,0,0,0,25,26,5,42,0,0,26,6,1,0,0,0,27,28,5,
        47,0,0,28,8,1,0,0,0,29,30,5,37,0,0,30,10,1,0,0,0,31,32,5,94,0,0,
        32,12,1,0,0,0,33,34,5,40,0,0,34,14,1,0,0,0,35,36,5,41,0,0,36,16,
        1,0,0,0,37,39,7,0,0,0,38,37,1,0,0,0,39,40,1,0,0,0,40,38,1,0,0,0,
        40,41,1,0,0,0,41,48,1,0,0,0,42,44,5,46,0,0,43,45,7,0,0,0,44,43,1,
        0,0,0,45,46,1,0,0,0,46,44,1,0,0,0,46,47,1,0,0,0,47,49,1,0,0,0,48,
        42,1,0,0,0,48,49,1,0,0,0,49,18,1,0,0,0,50,52,7,1,0,0,51,50,1,0,0,
        0,52,53,1,0,0,0,53,51,1,0,0,0,53,54,1,0,0,0,54,55,1,0,0,0,55,56,
        6,9,0,0,56,20,1,0,0,0,5,0,40,46,48,53,1,6,0,0
    ]

class ExprLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    PLUS = 1
    MINUS = 2
    MUL = 3
    DIV = 4
    MOD = 5
    POW = 6
    LPAREN = 7
    RPAREN = 8
    NUMBER = 9
    WS = 10

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'+'", "'-'", "'*'", "'/'", "'%'", "'^'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>",
            "PLUS", "MINUS", "MUL", "DIV", "MOD", "POW", "LPAREN", "RPAREN", 
            "NUMBER", "WS" ]

    ruleNames = [ "PLUS", "MINUS", "MUL", "DIV", "MOD", "POW", "LPAREN", 
                  "RPAREN", "NUMBER", "WS" ]

    grammarFileName = "Expr.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


