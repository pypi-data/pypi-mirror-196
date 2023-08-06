# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_dict']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1,<2']

setup_kwargs = {
    'name': 'pydantic-dict-encoders',
    'version': '0.1',
    'description': 'Pydantic mixins for support custom encoding dict',
    'long_description': '# Pydantic Dict Encoders\n\nSimple wrapper of pydantic for support custom dict encoders like json encoders\n',
    'author': 'Ivan Galin',
    'author_email': 'i.galin@devartsteam.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
