"""
my_runner.py


created at 2026-07-27
"""

from antlr4 import CommonTokenStream, InputStream

if "." in __name__:
    from .CSVLexer import CSVLexer
    from .CSVParser import CSVParser
    from .CSVVisitor import CSVVisitor
else:
    from CSVLexer import CSVLexer
    from CSVParser import CSVParser
    from CSVVisitor import CSVVisitor


class CSVToPythonVisitor(CSVVisitor):
    # 访问入口 rows : hdr row+ ;
    def visitRows(self, ctx: CSVParser.RowsContext):
        # 1. 获取表头列表
        headers = self.visit(ctx.hdr())

        # 2. 遍历所有数据行并与表头映射为字典
        data_rows = []
        for row_ctx in ctx.row():
            row_values = self.visit(row_ctx)
            # 将表头和当前行的数据打包成字典
            row_dict = dict(zip(headers, row_values))
            data_rows.append(row_dict)

        return data_rows

    # 访问表头 hdr : row ;
    def visitHdr(self, ctx: CSVParser.HdrContext):
        # 直接复用 row 的访问逻辑
        return self.visit(ctx.row())

    # 访问行 row : field (',' field)* '\r'? '\n' ;
    def visitRow(self, ctx: CSVParser.RowContext):
        # 遍历当前行中的所有字段，返回一个列表
        return [self.visit(field_ctx) for field_ctx in ctx.field()]

    # 访问字段 field : TEXT | STRING | ;
    def visitField(self, ctx: CSVParser.FieldContext):
        if ctx.TEXT():
            return ctx.TEXT().getText()
        elif ctx.STRING():
            raw_val = ctx.STRING().getText()
            # 去掉前后的双引号，并将中间的双双引号 "" 替换为单双引号 "
            return raw_val[1:-1].replace('""', '"')
        else:
            # 空字段返回空字符串
            return ""


def parse_csv(data):
    # 1. 创建输入流
    input_stream = InputStream(data)

    # 2. 词法分析
    lexer = CSVLexer(input_stream)
    token_stream = CommonTokenStream(lexer)

    # 3. 语法分析
    parser = CSVParser(token_stream)
    tree = parser.rows()  # 从 rows 规则开始解析

    # 4. 使用 Visitor 转换为 Python 对象
    visitor = CSVToPythonVisitor()
    result = visitor.visit(tree)

    return result
