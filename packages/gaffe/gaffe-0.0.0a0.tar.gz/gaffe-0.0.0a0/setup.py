# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gaffe']

package_data = \
{'': ['*']}

install_requires = \
['typing_extensions>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'gaffe',
    'version': '0.0.0a0',
    'description': 'Better exceptions for python.',
    'long_description': '# gaffe\n',
    'author': 'Dawid Kraczkowski',
    'author_email': 'dawid.kraczkowski@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kodemore/gaffe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
