# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['landfire', 'landfire.product']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.2.0',
 'pandas-stubs>=1.5.3.230304,<2.0.0.0',
 'pydantic>=1.10',
 'requests>=2.28.2,<3.0.0']

extras_require = \
{'geospatial': ['geojson>=3.0.0', 'geopandas>=0.12.0']}

setup_kwargs = {
    'name': 'landfire',
    'version': '0.2.1',
    'description': 'Landfire',
    'long_description': '# Landfire\n\n[![PyPI](https://img.shields.io/pypi/v/landfire.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/landfire.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/landfire)][python version]\n[![License](https://img.shields.io/pypi/l/landfire)][license]\n\n[![Read the documentation at https://landfire-python.readthedocs.io/](https://img.shields.io/readthedocs/landfire-python/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/FireSci/landfire-python/workflows/tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/FireSci/landfire-python/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/landfire/\n[status]: https://pypi.org/project/landfire/\n[python version]: https://pypi.org/project/landfire\n[read the docs]: https://landfire-python.readthedocs.io/\n[tests]: https://github.com/FireSci/landfire-python/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/FireSci/landfire-python\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Landfire_ via [pip] from [PyPI]:\n\n```console\n$ pip install landfire\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome. To learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Landfire_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n[pypi]: https://pypi.org/\n[file an issue]: https://github.com/FireSci/landfire-python/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/FireSci/landfire-python/blob/main/LICENSE\n[contributor guide]: https://github.com/FireSci/landfire-python/blob/main/CONTRIBUTING.md\n[command-line reference]: https://landfire-python.readthedocs.io/en/latest/usage.html\n',
    'author': 'FireSci',
    'author_email': 'support@firesci.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/FireSci/landfire-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
