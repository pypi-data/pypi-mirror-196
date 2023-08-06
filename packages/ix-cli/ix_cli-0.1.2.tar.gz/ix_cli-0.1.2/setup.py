# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ix_cli']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['ix = ix_cli.cli:app']}

setup_kwargs = {
    'name': 'ix-cli',
    'version': '0.1.2',
    'description': '',
    'long_description': '# A rich CLI template for pastebin CLI tools\n\nix is a command line interface for [ix.io](https://ix.io), a pastebin service.\n\nI tried to make this CLI as "reusable" as possible, so that you can clone this repository and use it as a template for your own pastebin CLI tool.\n\n## How to use this template\n\n1. Clone this repository\n2. Rename the `ix_cli` directory to the name of your pastebin service\n3. Replace the variable `PROVIDER_URL` in `ix_cli/utils.py` with the URL of your pastebin service (e.g. `https://paste.example.com`)\n4. Replace the name of the app in `pyproject.toml` with the name of your pastebin service in both the `name` and `[tool.poetry.scripts]` sections\n5. Install [poetry](https://python-poetry.org) and run `poetry install` to install the dependencies\n6. Run a basic command to make sure everything works: `<new-app-name> s "Hello, world!"`\n7. Edit the README to your liking\n8. Commit your changes and push them to your repository\n9. Publish your app to [PyPI](https://pypi.org) using `poetry build` and `poetry publish`\n\n## Installation\n\n### Using pip\n\n```bash\npip install ix-cli\n```\n\n### Cloning the repository\n\n```bash\ngit clone https://github.com/arnos-stuff/ix.git\n```\n\n## Basic usage\n\n### As a Python module\n\n```python\nfrom ix_cli import uploadFromFile, uploadFromStdin, download, getHistory\n\n# Upload from stdin\nurl = uploadFromStdin("Hello, world!")\nprint(url)\n\n# Upload from file\nurl = uploadFromFile("README.md")\nprint(url)\n\n# Download\ndata = download(url)\nprint(data)\n```\n\n### As a CLI tool\n\nUsing ix is simple. Just pipe some text into it:\n\n```bash\necho "Hello, world!" | ix s\n```\n\nThis will print the URL of the paste to stdout. You can also use ix to upload files:\n\n```bash\nix f README.md\n```\n\nThis CLI has an extra feature: it stores the past 100 URLs in a local cache. You can use this to quickly access your pastes:\n\n```bash\nix h\n```\n\nThis will print a list of your pastes, with the most recent at the top. You also have the option to limit the number of pastes shown:\n\n```bash\nix h -n 3\n```\n\nThis will print the 3 most recent pastes.\n\n## Getting the data back\n\nYou can use ix to retrieve the data from a paste by using the `g` command:\n\n```bash\nix g https://ix.io/1QZp\n```\n\nor simply\n\n```bash\nix g 1QZp\n```\n\nThis will print the contents of the paste to stdout.\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n',
    'author': 'arnos-stuff',
    'author_email': 'bcda0276@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/arnos-stuff/ix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
