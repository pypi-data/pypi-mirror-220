# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uqpylab', 'uqpylab.test']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'ipython>=8.7.0,<9.0.0',
 'ipywidgets>=8.0.4,<9.0.0',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.21.6,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'plotly>=5.11.0,<6.0.0',
 'requests>=2.28.2,<3.0.0',
 'scipy>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'uqpylab',
    'version': '0.95',
    'description': 'Official UQCloud python client: cloud-based uncertainty quantification in python with UQLab.',
    'long_description': 'None',
    'author': 'C. Lataniotis',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
