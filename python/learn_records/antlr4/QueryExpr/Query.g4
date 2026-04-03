grammar Query;

// --- Parser Rules (语法规则) ---
query: item* EOF ;
// item 现在可以是正常的 WORD，也可以是捕获到的非法字符 ERR
item: WORD | ERR ;

// --- Lexer Rules (词法规则) ---
WORD: [a-zA-Z0-9+/=._%\-]+ ;

// 忽略空白字符和指定分隔符
SEP: [;, \t\r\n]+ -> skip ;

// 匹配任何不属于上述规则的非法字符（去掉了 -> skip）
ERR: . ;