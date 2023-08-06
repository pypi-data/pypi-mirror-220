# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aprs_tocall']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0.1,<7.0.0']

entry_points = \
{'console_scripts': ['aprs_tocall = aprs_tocall:__main__.main']}

setup_kwargs = {
    'name': 'aprs-tocall',
    'version': '0.1.2',
    'description': 'Parses APRS "tocalls" or tocalls.txt / tocalls.yaml easily in Python',
    'long_description': 'aprs_tocall\n==\n\nInstall\n--\n\n```sh\npip install aprs_tocall\n```\n\nUsage\n--\n```python\nfrom aprs_tocall import Parser\ntocalls = Parser(offline=False) \n# Setting offline to False will use the online \n# yaml file, while offline=True (default) will \n# use the distributed version\ntocalls.lookup("APWEEA")\n# returns \n# {\n#   \'tocall\': \'APWEE?\',\n#   \'vendor\': \'Tom Keffer and Matthew Wall\',\n#   \'model\': \'WeeWX Weather Software\',\n#   \'class\': \'software\', \n#   \'os\': \'Linux/Unix\'\n# }\n```\n',
    'author': 'xss',
    'author_email': 'michaela@michaela.lgbt',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xssfox/aprs_tocall',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
