"""
09_wait_with_while_pending.py


created at 2026-04-08
"""

import asyncio

import aiohttp
from utils import fetch_status


async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://www.example.com"
        pending = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
        ]
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            print(f"Done task count: {len(done)}")
            print(f"Pending task count: {len(pending)}")

            for done_task in done:
                print(await done_task)


if __name__ == "__main__":
    asyncio.run(main())
