"""
csv2_loader.py


created at 2026-07-30
"""

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

    def __init__(self):
        self.rows = []
        self.headers: list | None = None
        self.current_row_field_values: list | None = None
