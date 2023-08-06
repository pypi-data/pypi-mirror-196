# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idasen_controller']

package_data = \
{'': ['*'], 'idasen_controller': ['example/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aiohttp>=3.8.4,<4.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'bleak>=0.19.5,<0.20.0']

entry_points = \
{'console_scripts': ['idasen-controller = idasen_controller.main:init']}

setup_kwargs = {
    'name': 'idasen-controller',
    'version': '2.0.2',
    'description': 'Command line tool for controlling the Ikea Idasen (Linak) standing desk',
    'long_description': 'None',
    'author': 'Rhys Tyers',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
