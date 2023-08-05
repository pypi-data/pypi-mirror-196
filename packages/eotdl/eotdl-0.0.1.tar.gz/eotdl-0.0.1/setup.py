# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eotdl']

package_data = \
{'': ['*']}

install_requires = \
['auth0-python>=4.0.0,<5.0.0',
 'pydantic>=1.10.5,<2.0.0',
 'pymongo>=4.3.3,<5.0.0']

setup_kwargs = {
    'name': 'eotdl',
    'version': '0.0.1',
    'description': 'Earth Obsertvation Training Datasets Lab',
    'long_description': '# eotdl \n\nThis is the main library for EOTDL.\n\n',
    'author': 'EarthPulse',
    'author_email': 'it@earthpulse.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
