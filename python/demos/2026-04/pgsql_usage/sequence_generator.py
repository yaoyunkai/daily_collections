"""
sequence_generator.py


created at 2026-04-23
"""

import datetime
import multiprocessing

from sqlalchemy import create_engine, text

ALPHABET = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"
BASE = len(ALPHABET)


def int_to_base34(num: int) -> str:
    if num == 0:
        return ALPHABET[0]
    res = []
    while num > 0:
        num, rem = divmod(num, BASE)
        res.append(ALPHABET[rem])
    return "".join(reversed(res))


def format_sequence(num: int) -> str:
    if num > 1336335:
        raise ValueError("Sequence exceeded maximum limit (ZZZZ) for this week.")
    b34_str = int_to_base34(num)
    return b34_str.zfill(4)  # 不足4位在前面补 '0'


def get_year_week() -> str:
    today = datetime.date.today()
    year, week, _ = today.isocalendar()

    yy = str(year)[-2:]
    ww = f"{week:02d}"
    return f"{yy}{ww}"


def generate_serial_number(engine, site_code: str) -> str:
    valid_sites = {"A", "B", "C", "D", "F"}
    if site_code not in valid_sites:
        raise ValueError(f"Invalid site code. Must be one of {valid_sites}")

    year_week = get_year_week()

    stmt = text("select get_next_serial_sequence(:site_code, :yw);")

    with engine.begin() as conn:
        result = conn.execute(stmt, {"site_code": site_code, "yw": year_week})
        seq_num = result.scalar()

    seq_str = format_sequence(seq_num)

    return f"{site_code}{year_week}{seq_str}"


def worker_task(args: tuple) -> list:
    """
    子进程执行的任务
    :param args: 包含 (进程ID, 站点代码, 生成数量)
    """
    process_id, site_code, count = args
    generated_sns = []

    engine = create_engine(
        "postgresql+psycopg://test1:test1@localhost:5432/demo1",
        connect_args={"options": "-c timezone=UTC", "connect_timeout": 3},
        echo=False,
        pool_size=5,
        max_overflow=10,
    )

    try:
        for _ in range(count):
            sn = generate_serial_number(engine, site_code)
            generated_sns.append(sn)
    except Exception as e:
        print(f"Process {process_id} encountered an error: {e}")
    finally:
        # 任务完成后释放该进程的连接池
        engine.dispose()

    print(f"Process {process_id} finished generating {len(generated_sns)} serial numbers.")
    return generated_sns


if __name__ == "__main__":
    NUM_PROCESSES = 10
    NUM_PER_PROCESS = 100
    TARGET_SITE = "A"

    print(f"Starting simulation: {NUM_PROCESSES} processes, each generating {NUM_PER_PROCESS} SNs...")

    tasks = [(i, TARGET_SITE, NUM_PER_PROCESS) for i in range(NUM_PROCESSES)]

    all_generated_sns = []
    with multiprocessing.Pool(processes=NUM_PROCESSES) as pool:
        results = pool.map(worker_task, tasks)

        for res_list in results:
            all_generated_sns.extend(res_list)

    total_generated = len(all_generated_sns)
    unique_sns = set(all_generated_sns)
    total_unique = len(unique_sns)

    print("\n" + "=" * 40)
    print("Simulation Completed!")
    print(f"Total SNs generated: {total_generated}")
    print(f"Total UNIQUE SNs:    {total_unique}")

    if total_generated == total_unique and total_generated == (NUM_PROCESSES * NUM_PER_PROCESS):
        print("✅ SUCCESS: No duplicate serial numbers were generated under high concurrency.")
        sorted_sns = sorted(list(unique_sns))
        print(f"Sample First 5: {sorted_sns[:5]}")
        print(f"Sample Last 5:  {sorted_sns[-5:]}")
    else:
        print("❌ FAILED: Duplicates found or missing serial numbers!")
