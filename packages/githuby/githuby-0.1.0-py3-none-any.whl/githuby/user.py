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

__all__ = ("User",)

from datetime import datetime
from typing import (
    Dict,
    Hashable,
    List,
    Optional,
    TYPE_CHECKING
)
import sys


if TYPE_CHECKING:
    from . import Repository


class User(Hashable):
    """
    Wrapper dataclass for a GitHub user.

    Operations
    ----------
    `hash(x)`
        Returns the users hash. This indirectly allows to compare
        two users with `x == y` and `x != y`
    `repr(x)`
        Returns the users representation
    `match x: ...` / `case GitHubUser(username="foo", id=1234): ...`
        Allows the user to be matched with a pattern. Only works
        on Python 3.10 and above.

    Attributes
    ----------
    admin: :class:`bool`
        Weather the user is a admin on GitHub or not.
    bio: Optional[:class:`str`]
        The users bio.
    blog: Optional[:class:`str`]
        An URL to the users blog. In reality, this can be any URL.
    created_at: :class:`datetime.datetime`
        A datetime object representing the time the user created
        its account.
    company: Optional[:class:`str`]
        The company the user works for.
    email: Optional[:class:`str`]
        The users public email address.
    hireable: :class:`bool`
        Weather the user is hireable or not.
    url: :class:`str`
        The users profile URL. This has the scheme `https://github.com/<username>`
    updated_at: :class:`datetime.datetime`
        A datetime object representing the time the account was
        last updated.
    username: :class:`str`
        The users username on GitHub.
    name: Optional[:class:`str`]
        The users real name if given.
    avatar_url: :class:`str`
        An URL to the users avatar.
    location: Optional[:class:`str`]
        The users location if given.
    id: :class:`int`
        The users ID on GitHub.
    followers: :class:`int`
        The amount of followers the user has.
    following: :class:`int`
        The amount of users the user is following.
    twitter_username: Optional[:class:`str`]
        The users Twitter username if given.
    repositories: :class:`list[Repository]`
        A list of all public repositories the user owns.
    raw_data: :class:`dict`
        The raw data returned by the GitHub API.
    """
    __slots__ = ("__user_data", "__repos")

    if sys.version_info.minor >= 10:
        __match_args__ = ("username", "id")

    def __init__(
        self,
        user_data: Dict[str, str],
        repos: Optional[List["Repository"]] = None
    ):
        self.__user_data = user_data
        self.__repos = list() if repos is None else repos

    def __repr__(self) -> str:
        return f"<{self.__class__.__qualname__} username={self.username!r}>"

    def __hash__(self) -> int:
        return hash((self.username, self.id, self.url))

    @property
    def _raw_data(self) -> Dict[str, str]:
        return self.__user_data.copy()

    @property
    def admin(self) -> bool:
        """
        Weather the user is a GitHub admin or not.
        """
        return bool(self.__user_data["site_admin"])

    @property
    def bio(self) -> Optional[str]:
        return self.__user_data["bio"]

    @property
    def blog(self) -> Optional[str]:
        return self.__user_data["blog"]

    @property
    def created_at(self) -> datetime:
        return datetime.strptime(self.__user_data["created_at"], "%Y-%m-%dT%H:%M:%SZ")

    @property
    def company(self) -> Optional[str]:
        return self.__user_data["company"]

    @property
    def email(self) -> Optional[str]:
        return self.__user_data["email"]

    @property
    def hireable(self) -> bool:
        return bool(self.__user_data["hireable"])

    @property
    def url(self) -> str:
        return self.__user_data["html_url"]

    @property
    def updated_at(self) -> datetime:
        return datetime.strptime(self.__user_data["updated_at"], "%Y-%m-%dT%H:%M:%SZ")

    @property
    def username(self) -> str:
        return self.__user_data["login"]

    @property
    def name(self) -> Optional[str]:
        """
        The real name of the user if given.
        """
        return self.__user_data["name"]

    @property
    def id(self) -> int:
        return int(self.__user_data["id"])

    @property
    def avatar_url(self) -> str:
        return self.__user_data["avatar_url"]

    @property
    def location(self) -> Optional[str]:
        return self.__user_data["location"]

    @property
    def followers(self) -> int:
        return int(self.__user_data["followers"])

    @property
    def following(self) -> int:
        return int(self.__user_data["following"])

    @property
    def repositories(self) -> List["Repository"]:
        """
        A tuple of the user's public repositories.
        """
        return self.__repos.copy()

    @property
    def repos(self) -> List["Repository"]:
        """
        Alias for :attr:`repositories`
        """
        return self.repositories

    @property
    def twitter_username(self) -> Optional[str]:
        return self.__user_data["twitter_username"]
