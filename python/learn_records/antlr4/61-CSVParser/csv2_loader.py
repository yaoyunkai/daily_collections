"""
csv2_loader.py


created at 2026-07-30
"""

from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker

if "." in __name__:
    from .CSV2Lexer import CSV2Lexer
    from .CSV2Listener import CSV2Listener
    from .CSV2Parser import CSV2Parser
    from .CSV2Visitor import CSV2Visitor
else:
    from CSV2Lexer import CSV2Lexer
    from CSV2Listener import CSV2Listener
    from CSV2Parser import CSV2Parser
    from CSV2Visitor import CSV2Visitor


class CSV2Loader(CSV2Listener):
    EMPTY = ""
    rows: list[dict[str, str]]
    header: list[str]
    current: list[str]

    def __init__(self):
        self.rows = list()

    def exitHdr(self, ctx: CSV2Parser.HdrContext):
        self.header = list()
        if self.current:
            for item in self.current:
                self.header.append(item)

    def enterRow(self, ctx: CSV2Parser.RowContext):
        self.current = list()

    def exitRow(self, ctx: CSV2Parser.RowContext):
        if ctx.parentCtx and ctx.parentCtx.getRuleIndex() == CSV2Parser.RULE_hdr:
            return

        row_map = {}
        for idx, value in enumerate(self.current):
            if idx < len(self.header):
                row_map[self.header[idx]] = value

        self.rows.append(row_map)

    def exitString(self, ctx: CSV2Parser.StringContext):
        self.current.append(ctx.STRING().getText())

    def exitText(self, ctx: CSV2Parser.TextContext):
        self.current.append(ctx.TEXT().getText())

    def exitEmpty(self, ctx: CSV2Parser.EmptyContext):
        self.current.append(self.EMPTY)


def runner(value: str):
    _is = InputStream(value)
    lexer = CSV2Lexer(_is)
    tokens = CommonTokenStream(lexer)

    parser = CSV2Parser(tokens)
    tree = parser.file_()
    walker = ParseTreeWalker()
    loader = CSV2Loader()
    walker.walk(loader, tree)

    # 输出结果
    print(loader.rows)


if __name__ == "__main__":
    fp = open("data.csv", mode="r", encoding="utf8")
    content = fp.read()

    runner(content)
    fp.close()
