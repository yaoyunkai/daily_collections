"""


Created at 2023/4/7
"""

import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)
    return delay


async def main():
    task1 = asyncio.create_task(say_after(1, 'hello'))

    task2 = asyncio.create_task(say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    ret = await task1
    print('task1 result is:', ret)
    await task2

    print(f"finished at {time.strftime('%X')}")


asyncio.run(main())
