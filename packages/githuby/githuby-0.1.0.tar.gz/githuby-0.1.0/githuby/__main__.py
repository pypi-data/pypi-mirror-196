"""
MIT License

Copyright (c) 2023 chr3st5an

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from pprint import pprint
from typing import List
import asyncio
import sys

from aiohttp import ClientSession

from . import fetch_user


async def fetcher(username: str, session: ClientSession) -> None:
    user = await fetch_user(username, session=session)

    if user is None:
        return print(f"User {username!r} not found.\n")

    print(f"User: {user.username} (#{user.id})\n")
    pprint(user.raw_data)
    print()


async def main(usernames: List[str]) -> None:
    async with ClientSession() as session:
        await asyncio.gather(*[
            fetcher(username, session=session) for username in usernames
        ])


asyncio.run(main(sys.argv[1:]))
