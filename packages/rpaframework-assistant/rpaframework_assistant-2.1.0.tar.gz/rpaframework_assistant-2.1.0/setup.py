# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['RPA', 'RPA.Assistant']

package_data = \
{'': ['*']}

install_requires = \
['flet==0.4.2',
 'robotframework>=4.0.0,!=4.0.1,<6.0.0',
 'rpaframework-core>=10.4.1,<11.0.0',
 'typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'rpaframework-assistant',
    'version': '2.1.0',
    'description': 'Interactive UI library for RPA Framework',
    'long_description': "rpaframework-assistant\n======================\nThis library allows creating dynamic dialogs during Robot Framework\nexecutions, which can be used for showing information to users and\nrequesting input from them. It's a part of `RPA Framework`_.\n\n\n.. _RPA Framework: https://rpaframework.org\n",
    'author': 'RPA Framework',
    'author_email': 'rpafw@robocorp.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://rpaframework.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
