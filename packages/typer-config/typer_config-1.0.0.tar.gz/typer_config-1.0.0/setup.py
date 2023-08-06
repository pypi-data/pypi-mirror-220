# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typer_config']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0,<1']

extras_require = \
{'all': ['toml>=0.10.2,<0.11.0', 'pyyaml>=6.0,<7.0', 'python-dotenv'],
 'python-dotenv': ['python-dotenv'],
 'toml': ['toml>=0.10.2,<0.11.0'],
 'yaml': ['pyyaml>=6.0,<7.0']}

setup_kwargs = {
    'name': 'typer-config',
    'version': '1.0.0',
    'description': 'Utilities for working with configuration files in typer CLIs. ',
    'long_description': '# typer-config\n\n[![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/maxb2/typer-config/ci.yml?branch=main&style=flat-square)](https://github.com/maxb2/typer-config/actions/workflows/ci.yml)\n[![Codecov](https://img.shields.io/codecov/c/github/maxb2/typer-config?style=flat-square)](https://app.codecov.io/gh/maxb2/typer-config)\n[![PyPI](https://img.shields.io/pypi/v/typer-config?style=flat-square)](https://pypi.org/project/typer-config/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/typer-config?style=flat-square)](https://pypi.org/project/typer-config/#history)\n[![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/typer-config?style=flat-square)](https://libraries.io/pypi/typer-config)\n\nThis is a collection of utilities to use configuration files to set parameters for a [typer](https://github.com/tiangolo/typer) CLI.\nIt is useful for typer commands with many options/arguments so you don\'t have to constantly rewrite long commands.\nThis package was inspired by [phha/click_config_file](https://github.com/phha/click_config_file) and prototyped in [this issue](https://github.com/tiangolo/typer/issues/86#issuecomment-996374166). It allows you to set values for CLI parameters using a configuration file. \n\n## Installation\n\n```bash\n$ pip install typer-config[all]\n```\n\n> **Note**: that will include libraries for reading from YAML, TOML, and Dotenv files as well.\n  Feel free to leave off the optional dependencies if you don\'t need those capabilities.\n\n## Usage\n\n```bash\n# Long commands like this:\n$ my-typer-app --opt1 foo --opt2 bar arg1 arg2\n\n# Can become this:\n$ my-typer-app --config config.yml\n```\n\n## Quickstart\n\nYou can use a decorator to quickly add a configuration parameter to your `typer` application:\n\n```py\nimport typer\nfrom typer_config import use_yaml_config\n\napp = typer.Typer()\n\n\n@app.command()\n@use_yaml_config() # MUST BE AFTER @app.command()\ndef main(...):\n    ...\n\nif __name__ == "__main__":\n    app()\n```\n\nYour typer command will now include a `--config CONFIG_FILE` option at the command line.\n\n> **Note**: this package also provides `@use_json_config`, `@use_toml_config`, and `@use_dotenv_config` for those file formats.\n> You can also use your own loader function and the `@use_config(loader_func)` decorator.\n\nSee the [documentation](https://maxb2.github.io/typer-config/latest/examples/simple_yaml/) for more examples using typer-config.',
    'author': 'Matt Anderson',
    'author_email': 'matt@manderscience.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://maxb2.github.io/typer-config/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
