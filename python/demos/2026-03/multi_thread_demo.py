"""
write your description here.

"""

import sys
import threading
import time

if hasattr(sys, "_is_gil_enabled") and not sys._is_gil_enabled():
    print("✅ 运行在无 GIL 模式下，多线程将利用多核 CPU")
else:
    print("⚠️ 警告：当前运行在标准 GIL 模式下，多线程不会提升 CPU 性能！")
    print("   请使用 python3.13t 或 uv run -p 3.13t 运行此脚本")


# CPU 密集型任务：计算平方和
def heavy_computation(task_id, iterations):
    result = 0
    for i in range(iterations):
        result += i * i
    print(f"任务 {task_id} 完成，结果片段：{result}")
    return result


def run_threads(num_threads, iterations_per_thread):
    threads = []
    start_time = time.time()

    for i in range(num_threads):
        # 创建线程
        t = threading.Thread(target=heavy_computation, args=(i, iterations_per_thread))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()
    print(f"\n总耗时：{end_time - start_time:.4f} 秒")


if __name__ == "__main__":
    # 设置任务量，确保足够大以看出区别
    THREAD_COUNT = 4
    ITERATIONS = 50_000_000  # 5 千万次计算

    print(f"开始运行 {THREAD_COUNT} 个线程，每个线程计算 {ITERATIONS} 次...")
    run_threads(THREAD_COUNT, ITERATIONS)
