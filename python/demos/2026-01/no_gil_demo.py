"""
free thread

"""
import math
import threading
import time


def find_primes_in_range(start, end, result_list: list):
    primes = []
    for num in range(start, end + 1):
        if num < 2:
            continue
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    result_list.extend(primes)


def run_single_threaded(start_range, end_range):
    print(f"--- 运行单线程版本 (范围: {start_range}-{end_range}) ---")
    start_time = time.time()
    all_primes = []
    find_primes_in_range(start_range, end_range, all_primes)
    end_time = time.time()
    print(f"单线程找到 {len(all_primes)} 个质数。")
    print(f"单线程耗时: {end_time - start_time:.4f} 秒")
    return end_time - start_time


def run_multi_threaded(start_range, end_range, num_threads):
    print(f"\n--- 运行多线程版本 ({num_threads} 线程, 范围: {start_range}-{end_range}) ---")
    start_time = time.time()

    # 存储所有线程找到的质数
    all_primes_threaded = []

    # 创建线程列表
    threads = []

    # 计算每个线程处理的范围
    range_size = (end_range - start_range + 1) // num_threads

    for i in range(num_threads):
        thread_start = start_range + i * range_size
        thread_end = thread_start + range_size - 1
        if i == num_threads - 1:  # 确保最后一个线程处理完所有剩余部分
            thread_end = end_range

        # 创建线程，并将结果列表作为参数传递
        thread = threading.Thread(target=find_primes_in_range, args=(thread_start, thread_end, all_primes_threaded))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"多线程找到 {len(all_primes_threaded)} 个质数。")
    print(f"多线程耗时: {end_time - start_time:.4f} 秒")
    return end_time - start_time


if __name__ == '__main__':
    run_single_threaded(1, 1000_0000)
    run_multi_threaded(1, 1000_0000, 4)
