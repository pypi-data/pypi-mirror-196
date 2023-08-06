# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['local_databricks', 'local_databricks.ldbutils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0',
 'pyspark>=3.3.2,<4.0.0',
 'python-dotenv>=0.19.1,<0.20.0',
 'structlog>=20.0.0,<21.0.0']

setup_kwargs = {
    'name': 'local-databricks',
    'version': '0.1.0',
    'description': 'Python library that provides a set of functions for handling running notebooks both locally and in Databricks using the same commands.',
    'long_description': 'None',
    'author': 'Santiago Armstrong',
    'author_email': 'santiagoarmstrong@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
