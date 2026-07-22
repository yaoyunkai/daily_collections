"""
Runner


"""

from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker

if "." in __name__:
    from .ArrayInitLexer import ArrayInitLexer
    from .ArrayInitListener import ArrayInitListener
    from .ArrayInitParser import ArrayInitParser
else:
    from ArrayInitLexer import ArrayInitLexer
    from ArrayInitListener import ArrayInitListener
    from ArrayInitParser import ArrayInitParser


def run_with_parser():
    my_input = "{1,2,3,4}"
    # print(my_input)
    _is = InputStream(my_input)
    lexer = ArrayInitLexer(_is)
    tokens = CommonTokenStream(lexer)

    parser = ArrayInitParser(tokens)
    tree = parser.init()
    print(tree.toStringTree(recog=parser))


class ShortToUnicodeString(ArrayInitListener):
    def enterInit(self, ctx: ArrayInitParser.InitContext):
        print('"', end="")

    def exitInit(self, ctx: ArrayInitParser.InitContext):
        print('"', end="")

    def enterValue(self, ctx: ArrayInitParser.ValueContext):
        # super().enterValue(ctx)
        value = ctx.INT()

        if value is not None:
            value = int(value.getText())
            print(f"\\u{value:04x}", end="")


def translate(value: str):
    my_input = InputStream(value)
    lexer = ArrayInitLexer(my_input)
    tokens = CommonTokenStream(lexer)

    parser = ArrayInitParser(tokens)
    tree = parser.init()

    walker = ParseTreeWalker()
    walker.walk(ShortToUnicodeString(), tree)
    print()


if __name__ == "__main__":
    # run_with_parser()
    translate("{1,2,4,{34,43},5}")
