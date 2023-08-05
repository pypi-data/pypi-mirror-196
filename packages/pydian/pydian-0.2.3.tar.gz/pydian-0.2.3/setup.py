# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydian', 'pydian.lib']

package_data = \
{'': ['*']}

install_requires = \
['jmespath>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'pydian',
    'version': '0.2.3',
    'description': 'Library for pythonic data interchange',
    'long_description': 'None',
    'author': 'Eric Pan',
    'author_email': 'eric.pan@stanford.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
