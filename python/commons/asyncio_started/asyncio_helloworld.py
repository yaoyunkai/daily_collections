"""


Created at 2023/4/7
"""

import asyncio


async def main():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')


asyncio.run(main())
