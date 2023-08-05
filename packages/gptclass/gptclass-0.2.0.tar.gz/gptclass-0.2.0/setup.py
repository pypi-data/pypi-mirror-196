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
    'version': '0.2.0',
    'description': 'A Python class that does what you need',
    'long_description': '# GPTClass\n**GPTClass** is a Python class that uses OpenAI\'s GPT to do what you need with minimal information.\n\n## Installation\n```bash\npip install gptclass\n```\n\n## Usage\n```python\n>>> import openai\n>>> openai.api_key = "..."\n\n>>> from gptclass import GPTClass\n>>> jack = GPTClass()\n\n>>> jack.add(1, 2)\n3\n>>> jack.n_unique([1, 2, 5, 5])\n3\n>>> jack.prime_numbers_below(10)\n[2, 3, 5, 7]\n>>> jack.count_vowels("Today I had a nice coffee!")\n10\n>>> jack.from_celsius_to_fahrenheit(25)\n77.0\n```\n\n## Notes\n- Inspired on: [davinci-functions](https://github.com/odashi/davinci-functions/tree/main)\n\n## Warning\n- The code produced may not be reliable and should be validated before executing it.',
    'author': 'Jaume Ferrarons',
    'author_email': 'jaume.ferrarons@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jaume-ferrarons/GPTClass',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
