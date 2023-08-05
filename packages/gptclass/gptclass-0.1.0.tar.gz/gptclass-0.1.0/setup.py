# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gptclass']

package_data = \
{'': ['*']}

install_requires = \
['diskcache>=5.4.0,<6.0.0', 'openai>=0.27.0,<0.28.0']

setup_kwargs = {
    'name': 'gptclass',
    'version': '0.1.0',
    'description': 'A Python that does what you need',
    'long_description': None,
    'author': 'Jaume Ferrarons',
    'author_email': 'jaume.ferrarons@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
