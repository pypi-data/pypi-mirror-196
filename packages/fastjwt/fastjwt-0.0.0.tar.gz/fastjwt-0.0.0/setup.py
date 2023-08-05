# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastjwt']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.5,<2.0.0', 'pyjwt[crypto]>=2.6.0,<3.0.0']

extras_require = \
{':python_full_version <= "3.9.0"': ['typing-extensions>=4.5.0,<5.0.0']}

setup_kwargs = {
    'name': 'fastjwt',
    'version': '0.0.0',
    'description': 'FastAPI Plugin for reusable JWT Authentication Management',
    'long_description': '# fastjwt\nFastAPI Plugin for reusable JWT Authentication Management\n\n![](./reports/docstr-badge.svg)',
    'author': 'Walid BENBIHI',
    'author_email': 'contact@ocarinow.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ocarinow/fastjwt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
