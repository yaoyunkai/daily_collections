"""


Created at 2023/4/7
"""

import asyncio


async def test_1():
    return '12345'


async def main():
    print('Hello ...')
    ret = await test_1()
    print('... World!')
    print('get result:', ret)


asyncio.run(main())
