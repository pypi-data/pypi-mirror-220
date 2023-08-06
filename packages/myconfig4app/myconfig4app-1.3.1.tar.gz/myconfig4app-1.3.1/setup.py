# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['myconfig']

package_data = \
{'': ['*']}

install_requires = \
['concurrent-log-handler>=0.9.20,<0.10.0',
 'path>=16.4.0,<17.0.0',
 'pyyaml>=6.0,<7.0',
 'singleton-decorator>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'myconfig4app',
    'version': '1.3.1',
    'description': '',
    'long_description': '# config\n\nBase config loader for app',
    'author': 'icersong',
    'author_email': 'icersong@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
