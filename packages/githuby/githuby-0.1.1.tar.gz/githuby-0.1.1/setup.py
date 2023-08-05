# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['githuby']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0']

setup_kwargs = {
    'name': 'githuby',
    'version': '0.1.1',
    'description': 'Simple package to get data about GitHub users',
    'long_description': '<h1 align="center">\n    githuby\n</h1>\n\n---\n\nSimple package for fetching user data from GitHub. This package provides\none simple async function `fetch_user()`, which wraps the data returned by the\nGitHub API into a `User` object which then can be used to easily access\nthe data. Repositories are also fetched and wrapped up into `Repository`\ninstances.\n\n## Installing\n\nPython3.8 or above is required.\n\n```sh\npip install githuby\n```\n\n## Quick Example\n\n```py\nfrom githuby import fetch_user\nimport asyncio\n\n\nasync def main():\n    user = await fetch_user("chr3st5an")\n\n    print(f"{user.username}#{user.id} has {len(user.repositories)} repos:")\n\n    for repo in user.repositories:\n        print(f"{repo.name}@{repo.url}")\n\n\nasyncio.run(main())\n```\n\n... or from the CLI\n\n```sh\npython -m githuby chr3st5an\n```\n',
    'author': 'Christian',
    'author_email': '64144555+chr3st5an@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/chr3st5an/githuby',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
