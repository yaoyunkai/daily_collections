"""
my_runner.py


created at 2026-07-30
"""

from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker

if "." in __name__:
    from .PropertyFileLexer import PropertyFileLexer
    from .PropertyFileListener import PropertyFileListener
    from .PropertyFileParser import PropertyFileParser
    from .PropertyFileVisitor import PropertyFileVisitor
else:
    from PropertyFileLexer import PropertyFileLexer
    from PropertyFileListener import PropertyFileListener
    from PropertyFileParser import PropertyFileParser
    from PropertyFileVisitor import PropertyFileVisitor


class MyPropertyFileVisitor(PropertyFileVisitor):
    def __init__(self):
        self.props = {}

    def visitProp(self, ctx: PropertyFileParser.PropContext):
        prop_id = ctx.ID().getText()
        prop_value = ctx.STRING().getText()
        if prop_id:
            self.props[prop_id] = prop_value


class PropertyFileLoader(PropertyFileListener):
    def __init__(self):
        self.props = {}

    def exitProp(self, ctx: PropertyFileParser.PropContext):
        prop_id = ctx.ID().getText()
        prop_val = ctx.STRING().getText()
        if prop_id:
            self.props[prop_id] = prop_val


def read_prop(value: str):
    _is = InputStream(value)
    lexer = PropertyFileLexer(_is)
    tokens = CommonTokenStream(lexer)
    parser = PropertyFileParser(tokens)

    tree = parser.file_()

    walker = ParseTreeWalker()
    loader = PropertyFileLoader()
    walker.walk(loader, tree)
    print(loader.props)


if __name__ == "__main__":
    demo1 = """user="parrt"
    machine="maniac"
    """
    read_prop(demo1)
