import asyncio

from utils import delay


async def main():
    sleep_for_three = asyncio.create_task(delay(3))
    print(type(sleep_for_three))
    result = await sleep_for_three
    print(result)


async def main1():
    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(3))
    sleep_once_more = asyncio.create_task(delay(3))

    # how to get result from here
    await sleep_for_three
    await sleep_again
    await sleep_once_more


if __name__ == '__main__':
    asyncio.run(main1())
