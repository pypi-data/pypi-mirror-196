# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['ctxwait']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'contextualwaiting',
    'version': '0.9.1',
    'description': 'Contextual Waiting',
    'long_description': '# Contextual Waiting Module - contextualwaiting\n\nThis package provides support for enhanced context based waiting.\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
