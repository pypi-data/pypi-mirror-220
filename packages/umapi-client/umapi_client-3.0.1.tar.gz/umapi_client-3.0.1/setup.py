# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['umapi_client']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT==2.4.0', 'cryptography>=38.0.4,<39.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'umapi-client',
    'version': '3.0.1',
    'description': 'Client for the User Management API (UMAPI) from Adobe - see https://adobe.ly/2h1pHgV',
    'long_description': "# umapi-client.py\n\nThis is a Python client for the User Management API from Adobe, aka the\n[UMAPI](https://www.adobe.io/products/usermanagement/docs/gettingstarted.html).\n\nThe User Management API is an Adobe-hosted network service which provides Adobe\nEnterprise customers the ability to manage their users. This client makes it\neasy to access the UMAPI from a local Python application.\n\nSee the [user guide](https://adobe-apiplatform.github.io/umapi-client.py/) for\nmore information.\n\nThis client is open source, maintained by Adobe, and distributed under the terms\nof the OSI-approved MIT license. Copyright (c) 2016-2023 Adobe Inc.\n\n# Compatibility\n\nThe `3.x` release branch is actively maintained. New users of the UMAPI client\nshould use the latest 3.x release. The `2.x` branch is still supported, but new\n2.x releases will only contain bug fixes. New features will only be developed\nfor 3.x.\n\nPull requests for 3.x should be made against the `v3` branch (the default\nbranch). Anything related to 2.x bugfixes should target `v2`.\n\n# Installation\n\n`umapi-client.py` is published to the Python Packaging Index.\n\nhttps://pypi.org/project/umapi-client/\n\nIt can be installed with pip:\n\n```\n$ pip install umapi-client\n```\n\nOr a dependency manager such as Poetry:\n\n```\n$ poetry add umapi-client\n```\n\n# Building\n\n[Poetry](https://python-poetry.org/) is required to build the package. Follow\nthe instructions documented on Poetry's website to install it on your system.\n\n1. Clone this repository\n   ```\n   $ git clone https://github.com/adobe-apiplatform/umapi-client.py\n   $ cd umapi-client.py\n   ```\n\n2. Install dependencies to virtual environment.\n   ```\n   $ poetry install\n   ```\n\n3. The `build` command will create a source package (`.tar.gz`) and a wheel file\n   (`.whl`) in the `dist` directory.\n\n   ```\n   $ poetry build\n   $ ls dist\n   umapi-client-3.0.1.tar.gz  umapi_client-3.0.1-py3-none-any.whl\n   ```\n\n4. Some of the packages required by this module use encryption, and so may\n   require you to do local builds of modules that use SSL. Typically, this will\n   require you to have a python installed that supports compiling extensions.\n\n5. Run tests with `pytest`.\n   ```\n   $ poetry run pytest\n   ```\n\n# Usage\n\nUsage documentation, as well as information about how to get client\ncredentials for use of the UMAPI, can be found in the\n[user guide](https://adobe-apiplatform.github.io/umapi-client.py/),\nwhose sources are in the `docs` directory of this repository.\n\n# License\n\nThis project is licensed under the MIT License. See [LICENSE](LICENSE) for more\ninformation.\n",
    'author': 'Andrew Dorton',
    'author_email': 'adorton@adobe.com',
    'maintainer': 'Andrew Dorton',
    'maintainer_email': 'adorton@adobe.com',
    'url': 'https://github.com/adobe-apiplatform/umapi-client.py/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
