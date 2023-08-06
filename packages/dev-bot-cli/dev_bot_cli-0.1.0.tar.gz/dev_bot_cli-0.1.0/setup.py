# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dev_bot_cli', 'dev_bot_cli.command']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'gitpython>=3.1.31,<4.0.0']

entry_points = \
{'console_scripts': ['devbot = dev_bot_cli.__main__:cli']}

setup_kwargs = {
    'name': 'dev-bot-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Cristiam Sosa',
    'author_email': 'cristiam.sosa@innocv.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
