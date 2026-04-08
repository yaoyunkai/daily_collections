"""
07_wait_demo.py


created at 2026-04-08
"""

import asyncio
import random


# 模拟向搜索引擎发起请求的异步函数
async def fetch_from_engine(engine_name: str, keyword: str) -> str:
    print(f"[*] 开始在 {engine_name} 中搜索: '{keyword}'...")

    try:
        delay = random.uniform(0.1, 2.5)
        await asyncio.sleep(delay)

        return f"[{engine_name}] 找到了 '{keyword}' 的相关数据 (耗时 {delay:.2f} 秒)"

    except asyncio.CancelledError:
        print(f"[-] {engine_name} 的搜索任务被强行中止。")
        raise  # 必须向上抛出 CancelledError，以确保任务正确结束


async def main():
    keyword = "Python 并发编程"
    engines = ["Google", "Bing", "DuckDuckGo", "Baidu"]

    tasks = [asyncio.create_task(fetch_from_engine(engine, keyword), name=engine) for engine in engines]

    print("\n=== 开始并发搜索 ===")
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # 3. 处理最先完成的任务结果
    # done 集合里包含了最先完成的 Task（通常只有一个，除非有多个任务在同一微秒内完成）
    first_finished_task = done.pop()
    result = first_finished_task.result()
    print(f"\n✅ 采用最快返回的结果:\n{result}\n")

    # 4. 核心逻辑：取消所有还在运行（未完成）的任务
    print("=== 开始清理其他未完成的任务 ===")
    for task in pending:
        task.cancel()  # 发送取消信号

    # 5. 可选但推荐的步骤：等待被取消的任务真正结束
    # 这一步是为了防止产生 "Task was destroyed but it is pending!" 的警告
    await asyncio.gather(*pending, return_exceptions=True)
    print("=== 所有清理工作完成 ===")


if __name__ == "__main__":
    # 运行主事件循环
    asyncio.run(main())
