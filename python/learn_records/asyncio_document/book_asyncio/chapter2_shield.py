"""
屏蔽取消请求


"""

import asyncio
from utils import delay


async def main():
    task = asyncio.create_task(delay(10))

    try:
        result = await asyncio.wait_for(asyncio.shield(task), 5)
        print(result)
    except asyncio.TimeoutError:
        print("Task took longer than five seconds!")
        result = await task
        print(result)


if __name__ == '__main__':
    asyncio.run(main())
