<h1 align="center">
    githuby
</h1>

---

Simple package for fetching user data from GitHub. This package provides
one simple async function `fetch_user()`, which wraps the data returned by the
GitHub API into a `User` object which then can be used to easily access
the data. Repositories are also fetched and wrapped up into `Repository`
instances.

## Installing

Python3.8 or above is required.

```sh
pip install githuby
```

## Quick Example

```py
from githuby import fetch_user
import asyncio


async def main():
    user = await fetch_user("chr3st5an")

    print(f"{user.username}#{user.id} has {len(user.repositories)} repos:")

    for repo in user.repositories:
        print(f"{repo.name}@{repo.url}")


asyncio.run(main())
```

... or from the CLI

```sh
python -m githuby chr3st5an
```
