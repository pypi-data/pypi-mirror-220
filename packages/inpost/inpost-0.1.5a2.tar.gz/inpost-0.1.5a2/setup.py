# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inpost', 'inpost.static', 'static']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.4.0,<10.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'arrow>=1.2.3,<2.0.0',
 'pytest>=7.4.0,<8.0.0',
 'qrcode>=7.3.1,<8.0.0']

setup_kwargs = {
    'name': 'inpost',
    'version': '0.1.5a2',
    'description': 'Asynchronous InPost package allowing you to manage existing incoming parcels without mobile app',
    'long_description': "[![CodeFactor](https://www.codefactor.io/repository/github/ifossa/inpost-python/badge)](https://www.codefactor.io/repository/github/ifossa/inpost-python)\n![Code Quality](https://github.com/ifossa/inpost-python/actions/workflows/lint.yml/badge.svg?barnch=main)\n![Todos](https://github.com/ifossa/inpost-python/actions/workflows/todos.yml/badge.svg?barnch=main)\n\n# Inpost Python\n\nFully async Inpost library using Python 3.10.\n\n\n## Documentation\n\n[Readthedocs.io](https://inpost-python.readthedocs.io/en/latest/)\n\n\n## Usage/Examples\n\n\n```python\nfrom inpost.api import Inpost\n\ninp = Inpost('555333444')\nawait inp.send_sms_code():\n...\nif await inp.confirm_sms_code(123321):\n   print('Congratulations, you initialized successfully!')\n```\n\n## Before you contribute\n\n![Contributors](https://contrib.rocks/image?repo=ifossa/inpost-python)\n\nInstall linters and checkers, unlinted pull requests will not be approved\n```commandline\npoetry run pre-commit install\n```\n\n## Authors\n\n- [@loboda4450](https://www.github.com/loboda4450)\n- [@mrkazik99](https://www.github.com/mrkazik99)\n\n\n## Used By\n\nThis project is used by the following repos:\n\n[Inpost Telegram Bot](https://github.com/loboda4450/inpost-telegram-bot)\n\n\n\n## 😂 Here is a random joke that'll make you laugh!\n![Jokes Card](https://readme-jokes.vercel.app/api)",
    'author': 'loboda4450',
    'author_email': 'loboda4450@gmail.com',
    'maintainer': 'loboda4450',
    'maintainer_email': 'loboda4450@gmail.com',
    'url': 'https://github.com/IFOSSA/inpost-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
