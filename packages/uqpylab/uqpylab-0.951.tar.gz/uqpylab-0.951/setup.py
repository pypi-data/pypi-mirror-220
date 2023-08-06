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
    'version': '0.951',
    'description': 'Official UQCloud python client: cloud-based uncertainty quantification in python with UQLab.',
    'long_description': '# UQ[py]Lab\nUQ[py]Lab is the official python client of the UQCloud project, which aims at providing a cloud-based, language agnostic API to the [UQLab](https://uqlab.com) uncertainty quantification framework. \n\nWhile still officially in a "beta testing" stage, UQ[py]Lab is close to its first public stable release, scheduled for Summer 2023.\n\n## Before you start\n\nBecause of its cloud-based nature, UQ[py]Lab requires an authentication token, which can be freely obtained by registering for beta testing at the UQ[py]Lab website: [https://uqpylab.uq-cloud.io](https://uqpylab.uq-cloud.io)\n\nAfter registration, you will find all the information you need to connect to the UQCloud servers at your personal profile page on [https://uqpylab.uq-cloud.io](https://uqpylab.uq-cloud.io).\n\n## Installation\n\nTo install the package in your local Python environment, execute the following command:\n\n```bash\npip install uqpylab\n```\n\n**Notes**:\n\n- UQ[py]Lab requires Python version >= 3.9\n- It is highly recommended to install UQ[py]Lab in a new Python virtual environment\n\n## First Steps\n\nTo get started with UQ[py]Lab, we strongly recommend new users to go peruse the following resources:\n\n1) The Getting started guide at: https://uqpylab.uq-cloud.io/getting-started\n\n2) Some examples, related to their application of interest: https://uqpylab.uq-cloud.io/examples\n\n## License\n\nUQ[py]Lab is free software, published under the open source [BSD 3-clause license](https://opensource.org/license/bsd-3-clause/).\n',
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
