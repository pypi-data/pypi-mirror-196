# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eotdl_cli']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['eotdl-cli = eotdl_cli.main:app']}

setup_kwargs = {
    'name': 'eotdl-cli',
    'version': '0.0.1',
    'description': '',
    'long_description': '# eotdl-cli\n\nThis is the CLI for EOTDL.\n\n',
    'author': 'EarthPulse',
    'author_email': 'it@earthpulse.es',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
