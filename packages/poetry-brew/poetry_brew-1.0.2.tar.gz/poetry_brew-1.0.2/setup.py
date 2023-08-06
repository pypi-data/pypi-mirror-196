# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['poetry_brew']

package_data = \
{'': ['*']}

install_requires = \
['dict-deep>=4.1.2,<5.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'poetry>=1.2,<2.0',
 'pydantic>=1.10.3,<2.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'poetry.application.plugin': ['brew = poetry_brew.plugin:PoetryBrewPlugin']}

setup_kwargs = {
    'name': 'poetry-brew',
    'version': '1.0.2',
    'description': 'Generate Homebrew formulae for Poetry projects',
    'long_description': "# poetry-brew\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/poetry-brew?logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/poetry-brew)\n[![PyPI](https://img.shields.io/pypi/v/poetry-brew?logo=pypi&color=green&logoColor=white&style=for-the-badge)](https://pypi.org/project/poetry-brew)\n[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/celsiusnarhwal/poetry-brew?logo=github&color=orange&logoColor=white&style=for-the-badge)](https://github.com/celsiusnarhwal/poetry-brew/releases)\n[![PyPI - License](https://img.shields.io/pypi/l/poetry-brew?color=03cb98&style=for-the-badge)](https://github.com/celsiusnarhwal/poetry-brew/blob/main/LICENSE.md)\n\npoetry-brew is a [Poetry](https://python-poetry.org/) plugin that generates Homebrew formulae for Poetry projects.\n\n## Installation\n\n```bash\npoetry self add poetry-brew\n```\n## Requirements\n\npoetry-brew can only generate formulae for packages that meet the following criteria:\n\n- The package must be published on PyPI.\n- `pyproject.toml` and `poetry.lock` must be present in the directory where `poetry brew` is run.\n- `pyproject.toml` must specify values for `tool.poetry.name`, `tool.poetry.version`,\n  and `tool.poetry.dependencies.python`.\n    - `tool.poetry.name` must be a case-insensitive match with the package's name on PyPI.\n    - `tool.poetry.version` must match a version of the package that has been published on PyPI.\n     For full usage information, run `poetry brew --help`.\n\n## Usage\n\n```bash\npoetry brew\n```\n\n`poetry brew` supports the `--with`, `--without`, and `--only` options, which function identically to `poetry install`.\nFor full usage information, run `poetry brew --help`.\n\n## Configuration\n\npoetry-brew can be configured through a `tool.brew.config` section in `pyproject.toml`.\n\n```toml\n[tool.brew.config]\ndependencies = []\n```\n\n### Supported Options\n\n- `dependencies` (`list`, default: `[]`): A list of other Homebrew formulae the package depends on.\n\n## License\n\npoetry-brew is licensed under the [MIT License](https://github.com/celsiusnarhwal/poetry-brew/blob/main/LICENSE.md).\n",
    'author': 'celsius narhwal',
    'author_email': 'hello@celsiusnarhwal.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/celsiusnarhwal/poetry-brew',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
