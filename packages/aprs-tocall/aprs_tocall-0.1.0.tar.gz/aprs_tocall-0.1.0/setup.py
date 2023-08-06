# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aprs_tocall']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0.1,<7.0.0']

setup_kwargs = {
    'name': 'aprs-tocall',
    'version': '0.1.0',
    'description': 'Parses APRS "tocalls" or tocalls.txt / tocalls.yaml easily in Python',
    'long_description': None,
    'author': 'xss',
    'author_email': 'michaela@michaela.lgbt',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xssfox/aprs_tocall',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
