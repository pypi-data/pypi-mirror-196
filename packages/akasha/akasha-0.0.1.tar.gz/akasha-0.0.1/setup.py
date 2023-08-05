# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['akasha']

package_data = \
{'': ['*']}

install_requires = \
['asyncache>=0.3.1,<0.4.0', 'cachetools>=5.2.0,<6.0.0']

setup_kwargs = {
    'name': 'akasha',
    'version': '0.0.1',
    'description': 'Python module for providing game information from different sources.',
    'long_description': '<p align="center">\n <img src="https://github.com/DEViantUA/Akasha-Terminal/blob/main/BannerAkasha.png?raw=true" alt="Баннер"/>\n</p>\n\n\n# Akasha-Terminal\nPython module for providing game information from different sources.\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/DEViantUA/Akasha-Terminal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
