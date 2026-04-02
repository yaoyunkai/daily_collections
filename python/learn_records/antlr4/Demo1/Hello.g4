grammar Hello;               // 1、定义文法的名字
// @header { package com.pioneeryi.learn.antlr; }  //2、java package

s  : 'hello' ID ;            // 3、匹配关键字hello和标志符
ID : [a-z]+ ;                // 标志符由小写字母组成
WS : [ \t\r\n]+ -> skip ;    // 4、跳过空格、制表符、回车符和换行符