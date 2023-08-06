# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['python_jmap', 'python_jmap.types']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=2.0.2,<3.0.0']

entry_points = \
{'console_scripts': ['python-jmap = python_jmap.__main__:main']}

setup_kwargs = {
    'name': 'python-jmap',
    'version': '0.0.4',
    'description': 'Python JMAP Bindings',
    'long_description': "# Python JMAP Bindings\n\n[![PyPI](https://img.shields.io/pypi/v/python-jmap.svg)][pypi status]\n[![Status](https://img.shields.io/pypi/status/python-jmap.svg)][pypi status]\n[![Python Version](https://img.shields.io/pypi/pyversions/python-jmap)][pypi status]\n[![License](https://img.shields.io/pypi/l/python-jmap)][license]\n\n[![Read the documentation at https://python-jmap.readthedocs.io/](https://img.shields.io/readthedocs/python-jmap/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/boopmail/python-jmap/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/boopmail/python-jmap/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi status]: https://pypi.org/project/python-jmap/\n[read the docs]: https://python-jmap.readthedocs.io/\n[tests]: https://github.com/boopmail/python-jmap/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/boopmail/python-jmap\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Python JMAP Bindings_ via [pip] from [PyPI]:\n\n```console\n$ pip install python-jmap\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Python JMAP Bindings_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/boopmail/python-jmap/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/boopmail/python-jmap/blob/main/LICENSE\n[contributor guide]: https://github.com/boopmail/python-jmap/blob/main/CONTRIBUTING.md\n[command-line reference]: https://python-jmap.readthedocs.io/en/latest/usage.html\n",
    'author': 'Josh Finch',
    'author_email': 'josh@boop.email',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/boopmail/python-jmap',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
