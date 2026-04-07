import asyncio

from utils import async_timed, delay


@async_timed()
async def main():
    task_one = asyncio.create_task(delay(2))
    task_two = asyncio.create_task(delay(3))

    # ret1 = await asyncio.create_task(delay(2))
    # ret2 = await asyncio.create_task(delay(3))
    # print(ret1)
    # print(ret2)

    await task_one
    await task_two

    print(task_one.result())
    print(task_two.result())


if __name__ == "__main__":
    asyncio.run(main())
