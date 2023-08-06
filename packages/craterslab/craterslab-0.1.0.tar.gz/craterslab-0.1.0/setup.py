# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['craterslab']

package_data = \
{'': ['*']}

install_requires = \
['keras>=2.13.1,<3.0.0',
 'matplotlib>=3.7.2,<4.0.0',
 'numpy>=1.24.0,<2.0.0',
 'opencv-python>=4.8.0,<5.0.0',
 'scikit-learn>=1.3.0,<2.0.0',
 'scipy>=1.11.1,<2.0.0',
 'tensorflow>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'craterslab',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Craters Morphology Analysis Tool\n\nA library to simplify the analysis of crater data from depth maps.\n\n## Installation\n\n```\n$ pip install craterslab\n```\n\n## Usage\n\nSee [this example](example.py).\n\n\n## (Optional) Contributing\n\n\n### Installing development dependencies\n```\n$ curl -sSL https://install.python-poetry.org | python3 -\n$ python3 -m venv .venv\n$ poetry install\n$ poetry shell\n```\n\n### Checking project code quality\n```\n$ make qa\n```',
    'author': 'Gustavo Viera López',
    'author_email': 'gvieralopez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gvieralopez/craters',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
