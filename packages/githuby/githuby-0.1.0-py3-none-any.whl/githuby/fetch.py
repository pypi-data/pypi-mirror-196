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

__all__ = ("fetch_user",)

from typing import Final, Optional
import async_timeout

from aiohttp import ClientSession

from .repository import Repository
from .user import User


BASE_URL: Final = "https://api.github.com"


async def fetch_user(
    username: str,
    *,
    session: Optional[ClientSession] = None,
    timeout: Optional[float] = None
) -> Optional["User"]:
    """
    |async|

    Fetches GitHub user using the `aiohttp` module.

    Parameters
    ----------
    username: :class:`str`
        The username of the user to fetch.
    session: Optional[:class:`aiohttp.ClientSession`]
        The session to use for the request. If not given, a
        new temporary session will be created.
    timeout: Optional[:class:`float`]
        The timeout for the request. If not given, the default
        timeout of the session will be used.

    Returns
    -------
    Optional[:class:`githuby.User`]
        The user, or `None` if the user was not found.

    Raises
    ------
    :exc:`asyncio.TimeoutError`
        The request timed out.
    """
    session_ = session or ClientSession()

    try:
        async with async_timeout.timeout(timeout):
            async with session_.get(f"{BASE_URL}/users/{username}") as u_response, \
                       session_.get(f"{BASE_URL}/users/{username}/repos") as r_response:

                if not (200 <= u_response.status <= 209):
                    return None

                user_data = await u_response.json()
                repo_data = await r_response.json()

            return User(user_data, [Repository(repo) for repo in repo_data])
    finally:
        if session is None:
            await session_.close()
