# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genai']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=8.10.0,<9.0.0', 'openai>=0.27.0,<0.28.0', 'vdom>=0.6,<0.7']

setup_kwargs = {
    'name': 'genai',
    'version': '0.12.0a0',
    'description': 'Generative AI for IPython (enhance your code cells)',
    'long_description': None,
    'author': 'Kyle Kelley',
    'author_email': 'rgbkrk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
