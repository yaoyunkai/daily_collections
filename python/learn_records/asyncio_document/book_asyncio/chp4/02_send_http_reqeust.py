"""
02_send_http_reqeust.py


created at 2026-04-08
"""

import asyncio

import aiohttp

# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)
from utils import async_timed


@async_timed()
async def fetch_status(session, url):
    async with session.get(url) as result:
        return result.status


async def main():
    async with aiohttp.ClientSession() as session:
        url = "https://www.example.com"
        status = await fetch_status(session, url)
        print(f"Get status: {status}")


asyncio.run(main())
