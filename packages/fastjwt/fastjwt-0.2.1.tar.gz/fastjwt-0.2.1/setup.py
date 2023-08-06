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
    'version': '0.2.1',
    'description': 'FastAPI Plugin for reusable JWT Authentication Management',
    'long_description': '# fastjwt\n\n<p style="text-align:center;">\n<a href="https://github.com/ocarinow/fastjwt" alt="Python"><img src="https://img.shields.io/pypi/pyversions/fastjwt" alt="Python Version" /></a>\n<a href="https://github.com/ocarinow/fastjwt/releases" alt="Releases"><img src="https://img.shields.io/github/v/release/ocarinow/fastjwt" alt="Latest Version" /></a>\n<a href="https://github.com/ocarinow/fastjwt/blob/main/LICENSE" alt="Licence"><img src="https://img.shields.io/github/license/ocarinow/fastjwt" alt="Licence" /></a>\n<a href="https://ocarinow.github.io/fastjwt/" alt="Documentation"><img src="https://img.shields.io/badge/docs-passing-brightgreen" alt="Documentation"></img></a></p>\n\n<p style="text-align:center;">\n<a href="https://github.com/ocarinow/fastjwt/actions" alt="Build Status"><img src="https://github.com/ocarinow/fastjwt/actions/workflows/python-release.yaml/badge.svg" alt="Build Status" /></a>\n<a href="https://github.com/ocarinow/fastjwt/actions" alt="Test Status"><img src="https://github.com/ocarinow/fastjwt/actions/workflows/python-test.yaml/badge.svg" alt="Test Status" /></a>\n<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://github.com/ocarinow/fastjwt/actions/workflows/python-publish.yaml/badge.svg" alt="Publish Status" /></a></p>\n\n<p style="text-align:center;">\n<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://raw.githubusercontent.com/ocarinow/fastjwt/dev/reports/coverage-badge.svg" alt="Coverage" /></a>\n<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://raw.githubusercontent.com/ocarinow/fastjwt/dev/reports/docstr-badge.svg" alt="Docstring" /></a>\n<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://raw.githubusercontent.com/ocarinow/fastjwt/dev/reports/flake8-badge.svg" alt="Flake8" /></a>\n<a href="https://github.com/ocarinow/fastjwt/actions" alt="Publish Status"><img src="https://raw.githubusercontent.com/ocarinow/fastjwt/dev/reports/tests-badge.svg" alt="Tests" /></a></p>\n\n\n<p style="text-align:center;">\n<a href="https://github.com/ocarinow/fastjwt/commits" alt="Stars"><img src="https://img.shields.io/github/commit-activity/m/ocarinow/fastjwt" alt="Commit Activity" /></a>\n<a href="https://github.com/ocarinow/fastjwt" alt="Repo Size"><img src="https://img.shields.io/github/repo-size/ocarinow/fastjwt" alt="Repo Size" /></a>\n<a href="https://github.com/ocarinow/fastjwt" alt="Issues"><img src="https://img.shields.io/github/issues/ocarinow/fastjwt" alt="Issues" /></a>\n<a href="https://github.com/ocarinow/fastjwt" alt="Pull Requests"><img src="https://img.shields.io/github/issues-pr/ocarinow/fastjwt" alt="Pull Requests" /></a>\n<a href="https://github.com/ocarinow/fastjwt" alt="Downloads"><img src="https://img.shields.io/github/downloads/ocarinow/fastjwt/total" alt="Downloads" /></a>\n</p>\n<p style="text-align:center;">\n<a href="https://github.com/ocarinow/fastjwt/stargazers" alt="Stars"><img src="https://img.shields.io/github/stars/ocarinow/fastjwt?style=social" alt="Stars" /></a>\n<a href="https://github.com/ocarinow/fastjwt" alt="Forks"><img src="https://img.shields.io/github/forks/ocarinow/fastjwt?style=social" alt="Forks" /></a>\n<a href="https://github.com/ocarinow/fastjwt/watchers" alt="Watchers"><img src="https://img.shields.io/github/watchers/ocarinow/fastjwt?style=social" alt="Watchers" /></a>\n</p>\n\n\nFastAPI Plugin for reusable JWT Authentication Management\n\n**fastjwt** enables easy JSON Web Tokens management within your FastAPI application.\n\n_fastjwt_ is heavily inspired from its Flask equivalent [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)\n\n**Documentation**: https://ocarinow.github.io/fastjwt/\n\n## Features\n\n- [x] Handles request for JWT in Cookies, Headers, Query Parameters and request Body\n- [ ] Handles Token Blocklist via custom callbacks\n- [ ] Handles User ORM via custom callbacks\n- [X] Protected routes\n- [X] Protected routes with fresh token/login\n- [X] Implicit/Explicit Token Refresh mechanisms\n- [ ] Partially protected routes\n\n## Setup\n\n### Requirements\n\nFastJWT is built on top of the following dependencies:\n\n- [FastAPI](https://github.com/tiangolo/fastapi) as web framework\n- [Pydantic](https://github.com/pydantic/pydantic) as data validation\n- [PyJWT](https://github.com/jpadilla/pyjwt) as python implementation of the JSON Web Token standard\n\nFastJWT also relies on [`typing-extensions`](https://pypi.org/project/typing-extensions/) for backward compatibility _(python3.9)_\n\n### Install\n\n```shell\n# With pip\npip install fastjwt\n# With poetry\npoetry add fastjwt\n# With pipenv\npipenv install fastjwt\n```\n\n## Example\n\n```py\nfrom fastapi import FastAPI, Depends\nfrom fastjwt import FastJWT\n\napp = FastAPI()\nsecurity = FastJWT()\n\n@app.get(\'/login\')\ndef login():\n    return security.create_access_token(uid=\'foo\')\n\n@app.get(\'/protected\', dependencies=[Depends(security.access_token_required())])\ndef protected():\n    return "This is a protected endpoint"\n```\n\n## Development\n\n> <span style="color:orange;">**WORK IN PROGRESS**</span>\n> \n> The development guide is not available yet\n\n## Contributing\n\n> <span style="color:orange;">**WORK IN PROGRESS**</span>\n> \n> The contribution guide is not available yet\n\n## License\n\n> <span style="color:orange;">**WORK IN PROGRESS**</span>\n> \n> The license is not available yet (open source MIT considered)',
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
