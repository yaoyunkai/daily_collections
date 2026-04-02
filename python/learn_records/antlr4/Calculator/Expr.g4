grammar Expr;

// --- Parser Rules (语法规则) ---
// 优先级由高到低排列
prog: expr EOF ;

expr
    : NUMBER                                         # Number
    | LPAREN expr RPAREN                             # Parens
    | expr MOD                                       # Percent     // (优先级最高：后缀百分比)
    | <assoc=right> expr POW expr                    # Pow         // (右结合：指数运算)
    | op=(PLUS | MINUS) expr                         # Unary       // (一元正负号)
    | expr op=(MUL | DIV | MOD) expr                 # MulDivMod   // (乘、除、求余)
    | expr op=(PLUS | MINUS) expr                    # AddSub      // (加、减)
    ;

// --- Lexer Rules (词法规则) ---
PLUS  : '+' ;
MINUS : '-' ;
MUL   : '*' ;
DIV   : '/' ;
MOD   : '%' ;
POW   : '^' ;
LPAREN: '(' ;
RPAREN: ')' ;

// 支持整数和小数
NUMBER: [0-9]+ ('.' [0-9]+)? ;

// 忽略空格、制表符和换行符
WS    : [ \t\r\n]+ -> skip ;