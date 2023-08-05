"""
githuby
~~~~~~~
A simple package for fetching user data from the GitHub API.

Simple Usage

    >>> from githuby import fetch_user
    >>> import asyncio
    >>> ...
    >>> await fetch_user("chr3st5an")

:author: chr3st5an
:license: MIT
"""

__author__ = "chr3st5an"
__license__ = "MIT"
__version__ = "0.1.0"

from .repository import *
from .fetch import *
from .user import *
