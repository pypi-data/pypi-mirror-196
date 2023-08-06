# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['structured_errors']

package_data = \
{'': ['*']}

install_requires = \
['typing_extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'structured-errors',
    'version': '0.0.1',
    'description': 'Better exceptions for python.',
    'long_description': '# Rift\n',
    'author': 'Dawid Kraczkowski',
    'author_email': 'dawid.kraczkowski@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kodemore/structured_errors',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
