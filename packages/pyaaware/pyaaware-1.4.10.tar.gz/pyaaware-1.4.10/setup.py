# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaaware']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyaaware',
    'version': '1.4.10',
    'description': 'Aaware Python development libraries',
    'long_description': 'None',
    'author': 'Jason Calderwood',
    'author_email': 'jason@aaware.com',
    'maintainer': 'Jason Calderwood',
    'maintainer_email': 'jason@aaware.com',
    'url': 'http://aaware.com',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
