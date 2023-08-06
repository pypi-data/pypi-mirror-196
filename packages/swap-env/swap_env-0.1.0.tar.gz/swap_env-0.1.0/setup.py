# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['swap_env']

package_data = \
{'': ['*']}

install_requires = \
['inquirerpy>=0.3.4,<0.4.0']

entry_points = \
{'console_scripts': ['swap-env = swap_env.cli:app']}

setup_kwargs = {
    'name': 'swap-env',
    'version': '0.1.0',
    'description': 'A simple CLI for swapping between .env files',
    'long_description': '# Swap Env\n\nA simple CLI for swapping between different `.env` files.\n',
    'author': 'Ben Berry-Allwood',
    'author_email': 'benberryallwood@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/benberryallwood/swap-env',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
