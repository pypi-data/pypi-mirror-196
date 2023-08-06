# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noble']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'noble',
    'version': '0.0.1',
    'description': 'Fast (indexed) bazel queries',
    'long_description': 'noble\n_________________\n\n[![PyPI version](https://badge.fury.io/py/noble.svg)](http://badge.fury.io/py/noble)\n[![Test Status](https://github.com/timothycrosley/noble/workflows/Test/badge.svg?branch=develop)](https://github.com/timothycrosley/noble/actions?query=workflow%3ATest)\n[![Lint Status](https://github.com/timothycrosley/noble/workflows/Lint/badge.svg?branch=develop)](https://github.com/timothycrosley/noble/actions?query=workflow%3ALint)\n[![codecov](https://codecov.io/gh/timothycrosley/noble/branch/main/graph/badge.svg)](https://codecov.io/gh/timothycrosley/noble)\n[![Join the chat at https://gitter.im/timothycrosley/noble](https://badges.gitter.im/timothycrosley/noble.svg)](https://gitter.im/timothycrosley/noble?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)\n[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.python.org/pypi/noble/)\n[![Downloads](https://pepy.tech/badge/noble)](https://pepy.tech/project/noble)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)\n_________________\n\n[Read Latest Documentation](https://timothycrosley.github.io/noble/) - [Browse GitHub Code Repository](https://github.com/timothycrosley/noble/)\n_________________\n\n**noble** Fast (indexed) bazel queries\n',
    'author': 'Timothy Crosley',
    'author_email': 'timothy.crosley@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
