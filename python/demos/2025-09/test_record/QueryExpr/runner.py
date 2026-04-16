import enum
import re

from antlr4 import CommonTokenStream, InputStream

if "." in __name__:
    from .QueryLexer import QueryLexer
    from .QueryParser import QueryParser
    from .QueryVisitor import QueryVisitor
else:
    from QueryLexer import QueryLexer
    from QueryParser import QueryParser
    from QueryVisitor import QueryVisitor


class QMode(enum.StrEnum):
    Normal = "N"
    Pattern = "P"


class QueryProcessor(QueryVisitor):
    def __init__(self):
        self.results = []
        self.has_error = False
        self.has_alnum = re.compile(r"[a-zA-Z0-9]")
        self.has_wildcard = re.compile(r"[_%]")

    def visitItem(self, ctx: QueryParser.ItemContext):
        if ctx.ERR():
            self.has_error = True
            return None

        if ctx.WORD():
            word = ctx.WORD().getText()
            if self.has_alnum.search(word):
                if self.has_wildcard.search(word):
                    self.results.append((QMode.Pattern, word))
                else:
                    self.results.append((QMode.Normal, word))

        return self.visitChildren(ctx)


def parse_query(query_str: str) -> list:
    """
    解析查询字符串并返回处理后的元组列表
    """
    if not query_str or not query_str.strip():
        return []

    input_stream = InputStream(query_str)
    lexer = QueryLexer(input_stream)

    # 移除默认的错误监听器，防止控制台打印 ANTLR 的默认警告
    lexer.removeErrorListeners()

    stream = CommonTokenStream(lexer)
    parser = QueryParser(stream)
    parser.removeErrorListeners()

    tree = parser.query()
    visitor = QueryProcessor()
    visitor.visit(tree)
    if visitor.has_error:
        return []
    return visitor.results


# ==========================================
# 测试用例 (验证你的所有例子)
# ==========================================
if __name__ == "__main__":
    test_cases = [
        ("ABC", [("N", "ABC")]),
        ("ABC_", [("P", "ABC_")]),
        ("ABC%", [("P", "ABC%")]),
        (" ABCD   ", [("N", "ABCD")]),
        ("ABCD;ABC", [("N", "ABCD"), ("N", "ABC")]),
        ("ABCD,BCD%", [("N", "ABCD"), ("P", "BCD%")]),
        ("ABC DEF-SDF", [("N", "ABC"), ("N", "DEF-SDF")]),
        ("ABC \n CDF", [("N", "ABC"), ("N", "CDF")]),
        ("         ", []),  # 全空白字符串
        ("    +++++", []),  # 纯符号，无效
        ("+++++%%%%%, ABCD", [("N", "ABCD")]),  # 前者纯符号无效，后者有效
    ]

    # fmt: off
    new_test_cases = [
        # ==========================================
        # 1. 基础正常词 (Normal) 测试
        # ==========================================
        ("A", [('N', 'A')]),                                # 单个字母
        ("123", [('N', '123')]),                            # 纯数字
        ("a-b+c=d/e.f", [('N', 'a-b+c=d/e.f')]),            # 包含所有允许的正常符号

        # ==========================================
        # 2. 基础模式匹配词 (Pattern) 测试
        # ==========================================
        ("_A", [('P', '_A')]),                              # _ 在开头
        ("%123", [('P', '%123')]),                          # % 在开头
        ("A_B%C", [('P', 'A_B%C')]),                        # 混合在中间
        ("A_", [('P', 'A_')]),                              # _ 在结尾

        # ==========================================
        # 3. 纯符号过滤 (Invalid) 测试 - 必须包含至少一个字母或数字
        # ==========================================
        ("+ - = / .", []),                                  # 纯正常符号，空格隔开
        ("++--==//..", []),                                 # 纯正常符号连写
        ("_ % _%", []),                                     # 纯模式匹配符号 (只有 _ 和 %)
        ("+_%.-", []),                                      # 正常符号与模式符号混合，但无字母数字

        # ==========================================
        # 4. 分隔符滥用与空白测试
        # ==========================================
        (";;, ,;; \t \n", []),                              # 全是分隔符
        ("A;;;B,,,C \n D", [('N', 'A'), ('N', 'B'), ('N', 'C'), ('N', 'D')]), # 多个分隔符连写
        (",; A ;, B ;,", [('N', 'A'), ('N', 'B')]),         # 首尾包含分隔符

        # ==========================================
        # 5. 混合复杂场景测试
        # ==========================================
        ("A+B, +++, C%", [('N', 'A+B'), ('P', 'C%')]),      # 正常词、纯符号(被丢弃)、模式词
        ("___, 123_, %%%, .a.", [('P', '123_'), ('N', '.a.')]), # 纯模式符号被丢弃
        ("+A, A+, .1.", [('N', '+A'), ('N', 'A+'), ('N', '.1.')]), # 符号在有效字符的边缘
        ("_%A_%", [('P', '_%A_%')]),                        # 模式符号包围有效字符

        # ==========================================
        # 6. 未定义字符/非法字符容错测试 (基于 ANTLR 的 ERR 规则)
        # 规则中未定义的字符（如 @, *, !, 中文等）会被当作 ERR skip 掉，从而起到隐式分隔的作用
        # ==========================================
        ("ABC@DEF", []),          # @ 被忽略，ABC 和 DEF 被拆分
        ("Hello*World", []),  # * 被忽略
        ("A!@#B$%^C", []),# 特殊符号被忽略，保留了 % 触发 Pattern
        ("测试ABC", []),                          # 中文不在规则内，被忽略

    ]
    # fmt: on

    for i, (input_str, expected) in enumerate(test_cases + new_test_cases, 1):
        result = parse_query(input_str)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"Test {i}: {status}")
        print(f"  Input   : {repr(input_str)}")
        print(f"  Output  : {result}")
        print("-" * 40)
