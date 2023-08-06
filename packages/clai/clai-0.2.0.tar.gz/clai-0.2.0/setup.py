# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clai', 'clai.ocr_drivers']

package_data = \
{'': ['*']}

install_requires = \
['PyAutoGUI>=0.9.53,<0.10.0',
 'PyWinCtl>=0.0.43,<0.0.44',
 'openai>=0.27.0,<0.28.0',
 'pytesseract>=0.3.10,<0.4.0']

entry_points = \
{'console_scripts': ['ai = clai:main', 'clai = clai:main']}

setup_kwargs = {
    'name': 'clai',
    'version': '0.2.0',
    'description': 'Command Line AI- this tool lets you call ChatGPT from a CLI',
    'long_description': '# clai\nCommand Line AI- this tool lets you call ChatGPT from a CLI. \n\nI\'m designing this to be used in conjunction with a fork of [shin][shin], which will allow you\nto call `clai` from any textbox in your computer. Finally, ChatGPT everywhere!\n\nThe long-term vision for this project is to add support for extracting context. For example, it would\nread the current text on a window and be able to add to it, or answer questions about it.\n\n_________________\n\n[![PyPI version](https://badge.fury.io/py/clai.svg)](http://badge.fury.io/py/clai)\n[![Test Status](https://github.com/apockill/clai/workflows/Test/badge.svg?branch=main)](https://github.com/apockill/clai/actions?query=workflow%3ATest)\n[![Lint Status](https://github.com/apockill/clai/workflows/Lint/badge.svg?branch=main)](https://github.com/apockill/clai/actions?query=workflow%3ALint)\n[![codecov](https://codecov.io/gh/apockill/clai/branch/main/graph/badge.svg)](https://codecov.io/gh/apockill/clai)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)\n_________________\n\n[Read Latest Documentation](https://apockill.github.io/clai/) - [Browse GitHub Code Repository](https://github.com/apockill/clai/)\n_________________\n\n## Installation\n\n1. The recommended installation method is to use `pipx`, via\n    ```bash\n    pipx install clai\n    ```\n   Optionally, install `tesseract` so that `clai` can read the screen context and send that along with requests:\n   ```bash\n   sudo apt install tesseract-ocr scrot\n   ```\n1. Then go to [OpenAI] and create an API Key. Once it\'s generated, add the following to \n   your `~/.profile`:\n   ```bash\n   export OPENAI_API_TOKEN=<paste here>\n   ```\n\n1. The best way to use this tool is in conjunction with the tool [shin][shin], which allows you\n   to run arbitrary bash commands in any textbox in a linux computer, using ibus. To use \n   that, install \'shin\' via the fork above, then configure\n   it in your `~/.profile` to call `clai` by default:\n   ```bash\n   export SHIN_DEFAULT_COMMAND="clai"\n   ```\n1. Log out then log back in for the changes to take effect!\n\n[OpenAI]: https://platform.openai.com/account/api-keys\n\n## Usage\nInvoke the assistant with the format `clai <your prompt>`. For example:\n```\nclai Write an email saying I\'ll be late to work because I\'m working on commandline AIs\n```\n\n\n## Development\n\n### Installing python dependencies\n```shell\npoetry install\n```\n\n### Running Tests\n```shell\npytest .\n```\n\n### Formatting Code\n```shell\nbash .github/format.sh\n```\n\n### Linting\n```shell\nbash .github/check_lint.sh\n```\n\n[shin]: https://github.com/apockill/shin\n',
    'author': 'apockill',
    'author_email': 'apocthiel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
