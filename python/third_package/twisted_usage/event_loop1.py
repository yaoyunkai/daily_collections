"""
file: event_loop1.py
Created by Libyao at 2023/4/12

事件驱动编程

异步编程


协议 传输 反应器 消费者 生产者

--------------------------------------------
1. 事件表示已经发生某些事情，程序应该对此作出反应
2. 事件处理程序构成了程序对事件的反应
3. 一个事件循环一直等待事件的触发


多路复用和多路分解

忙等: 程序忙碌地等待着


"""

import sys

line = sys.stdin.readline().strip()

if line == 'h':
    print('hello')
else:
    print('world')
