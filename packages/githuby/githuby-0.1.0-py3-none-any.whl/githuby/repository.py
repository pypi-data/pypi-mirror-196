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

__all__ = ("Repository",)

from typing import (
    Any,
    Dict,
    Hashable,
    List,
    Literal,
    Optional
)
from datetime import datetime
import sys


class Repository(Hashable):
    """
    Wrapper dataclass for a GitHub repository.

    Operations
    ----------
    `hash(x)`
        Returns the hash of the repository.
    `repr(x)`
        Returns the representation of the repository.
    `match x: ...` / `case Repository(name="foo", owner="chr3st5an"): ...`
        Allows the repository to be matched with a pattern. Only works
        on Python 3.10 and above.

    Attributes
    ----------
    allow_forks: :class:`bool`
        Weather the repository allows forks or not.
    created_at: :class:`datetime.datetime`
        A datetime object representing the time the repository was created.
    default_branch: :class:`str`
        The default branch of the repository.
    description: Optional[:class:`str`]
        The description of the repository.
    forks: :class:`int`
        The amount of forks the repository has.
    has_discussions: :class:`bool`
        Weather the repository has discussions enabled or not.
    has_downloads: :class:`bool`
        Weather the repository has downloads enabled or not.
    has_issues: :class:`bool`
        Weather the repository has issues enabled or not.
    has_pages: :class:`bool`
        Weather the repository has pages enabled or not.
    has_projects: :class:`bool`
        Weather the repository has projects enabled or not.
    has_wiki: :class:`bool`
        Weather the repository has wiki enabled or not.
    homepage: Optional[:class:`str`]
        The homepage of the repository.
    url: :class:`str`
        The URL to the repository on GitHub.
    language: Optional[:class:`str`]
        The main programming language of the repository.
    name: :class:`str`
        The name of the repository.
    owner: :class:`str`
        The username of the owner of the repository.
    is_archived: :class:`bool`
        Weather the repository is archived or not.
    is_disabled: :class:`bool`
        Weather the repository is disabled or not.
    is_fork: :class:`bool`
        Weather the repository is a fork or not.
    is_private: :class:`bool`
        Weather the repository is private or not.
    is_template: :class:`bool`
        Weather the repository is a template or not.
    pushed_at: :class:`datetime.datetime`
        A datetime object representing the time the repository was last pushed to.
    size: :class:`int`
        The size of the repository in kilobytes.
    stars: :class:`int`
        The amount of stars the repository has.
    topics: List[:class:`str`]
        A list of topics the repository has.
    watchers: :class:`int`
        The amount of watchers the repository has.
    visibility: :class:`str`
        The visibility of the repository, can be either `public`,
        `private` or `internal`.
    url: :class:`str`
        The URL to the repository on GitHub.
    updated_at: :class:`datetime.datetime`
        A datetime object representing the time the repository was last updated.
    """
    __slots__ = ("__repo_data",)

    if sys.version_info.minor >= 10:
        __match_args__ = ("name", "owner")

    def __init__(self, repo_data: Dict[str, Any]):
        self.__repo_data = repo_data

    def __repr__(self) -> str:
        return f"<{self.__class__.__qualname__} name={self.name!r}>"

    def __hash__(self) -> int:
        return hash((self.name, self.owner, self.url))

    @property
    def _raw_data(self) -> Dict[str, Any]:
        return self.__repo_data.copy()

    @property
    def allow_forks(self) -> bool:
        return bool(self.__repo_data["allow_forks"])

    @property
    def created_at(self) -> datetime:
        return datetime.strptime(self.__repo_data["created_at"], "%Y-%m-%dT%H:%M:%SZ")

    @property
    def default_branch(self) -> str:
        return self.__repo_data["default_branch"]

    @property
    def description(self) -> Optional[str]:
        return self.__repo_data["description"]

    @property
    def forks(self) -> int:
        return int(self.__repo_data["forks_count"])

    @property
    def has_discussions(self) -> bool:
        return bool(self.__repo_data["has_discussions"])

    @property
    def has_downloads(self) -> bool:
        return bool(self.__repo_data["has_downloads"])

    @property
    def has_issues(self) -> bool:
        return bool(self.__repo_data["has_issues"])

    @property
    def has_pages(self) -> bool:
        return bool(self.__repo_data["has_pages"])

    @property
    def has_projects(self) -> bool:
        return bool(self.__repo_data["has_projects"])

    @property
    def has_wiki(self) -> bool:
        return bool(self.__repo_data["has_wiki"])

    @property
    def homepage(self) -> str:
        return self.__repo_data["homepage"]

    @property
    def language(self) -> Optional[str]:
        return self.__repo_data["language"]

    @property
    def name(self) -> str:
        return self.__repo_data["name"]

    @property
    def open_issues(self) -> int:
        return int(self.__repo_data["open_issues_count"])

    @property
    def owner(self) -> str:
        return self.__repo_data["owner"]["login"]  # type: ignore

    @property
    def is_archived(self) -> bool:
        return bool(self.__repo_data["archived"])

    @property
    def is_fork(self) -> bool:
        return bool(self.__repo_data["fork"])

    @property
    def is_disabled(self) -> bool:
        return bool(self.__repo_data["disabled"])

    @property
    def is_private(self) -> bool:
        return bool(self.__repo_data["private"])

    @property
    def is_template(self) -> bool:
        return bool(self.__repo_data["is_template"])

    @property
    def pushed_at(self) -> datetime:
        return datetime.strptime(self.__repo_data["pushed_at"], "%Y-%m-%dT%H:%M:%SZ")

    @property
    def size(self) -> int:
        return int(self.__repo_data["size"])

    @property
    def stars(self) -> int:
        return int(self.__repo_data["stargazers_count"])

    @property
    def topics(self) -> List[str]:
        return list(self.__repo_data["topics"])

    @property
    def url(self) -> str:
        return self.__repo_data["html_url"]

    @property
    def updated_at(self) -> datetime:
        return datetime.strptime(self.__repo_data["updated_at"], "%Y-%m-%dT%H:%M:%SZ")

    @property
    def visibility(self) -> Literal["public", "private", "internal"]:
        return self.__repo_data["visibility"]  # type: ignore

    @property
    def watchers(self) -> int:
        return int(self.__repo_data["watchers_count"])
