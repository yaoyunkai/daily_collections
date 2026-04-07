"""
chp2_21_create_event_loop.py

created at 2026-04-07
"""

import asyncio


async def main():
    await asyncio.sleep(2)


loop = asyncio.new_event_loop()

try:
    loop.run_until_complete(main())
finally:
    loop.close()
