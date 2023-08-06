# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['suinspy', 'suinspy.types', 'suinspy.utils']

package_data = \
{'': ['*']}

install_requires = \
['pysui>=0.27.1,<0.28.0', 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'suinspy',
    'version': '0.1.0',
    'description': 'Sui Name Service Python SDK Client',
    'long_description': None,
    'author': 'andreidev1',
    'author_email': 'd.andrei01@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
