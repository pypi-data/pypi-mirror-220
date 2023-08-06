# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idkwhttph']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'idkwhttph',
    'version': '0.2.8',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
