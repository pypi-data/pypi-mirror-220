# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepbookpy', 'deepbookpy.utils']

package_data = \
{'': ['*']}

install_requires = \
['pysui>=0.29.0,<0.30.0']

setup_kwargs = {
    'name': 'deepbookpy',
    'version': '0.2.0',
    'description': 'Sui Deepbook Python SDK',
    'long_description': None,
    'author': 'andreidev1',
    'author_email': 'andreid.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
