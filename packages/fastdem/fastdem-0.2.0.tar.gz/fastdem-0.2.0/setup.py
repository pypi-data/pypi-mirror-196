# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastdem']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['fastdem = fastdem.__main__:app']}

setup_kwargs = {
    'name': 'fastdem',
    'version': '0.2.0',
    'description': '',
    'long_description': '',
    'author': 'wanqiang.liu',
    'author_email': 'wanqiang.liu@freetech.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
