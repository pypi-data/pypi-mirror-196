# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['adler']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'adler',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Pradipta Deb',
    'author_email': 'pradipta.deb@vadesecure.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
