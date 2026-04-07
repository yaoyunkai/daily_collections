"""
00_daemon_with_join.py

给 join() 加上一个超时时间（Timeout）：t.join(timeout=N)。

t.join(timeout=2.0) 的真正意思是：“主线程在这里最多只等 2 秒。
2 秒一到，主线程就不等了，主线程自己继续往下执行代码。但是，那个子线程依然在后台继续活着、继续运行！”


============================================================
t.join() (不带参数) + daemon=True = 毫无意义的自相矛盾
t.join(timeout=N) + daemon=True = 非常优雅的退出策略。


created at 2026-04-07
"""

import threading
import time


def background_task():
    print("后台任务：开始工作...")
    for i in range(5):
        time.sleep(1)
        print(f"后台任务：正在处理第 {i + 1} 步...")
    print("后台任务：工作圆满完成！")


# 1. 设置为守护线程 (Daemon)
t = threading.Thread(target=background_task, daemon=True)
t.start()

try:
    # 主线程模拟做一些其他事情
    time.sleep(2)
    print("主线程：我的工作做完了，准备退出。")

except KeyboardInterrupt:
    print("\n主线程：收到 Ctrl+C！准备退出。")

finally:
    print("主线程：我最多再等后台任务 2 秒钟...")

    # 2. 配合带超时的 join 使用
    t.join(timeout=2.0)

    if t.is_alive():
        print("主线程：2秒到了，后台任务还没做完，不管了，强制拉闸！")
    else:
        print("主线程：后台任务在2秒内自己做完了，完美退出。")
