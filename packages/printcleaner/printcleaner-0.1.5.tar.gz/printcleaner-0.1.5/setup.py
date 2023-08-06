# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['printcleaner']

package_data = \
{'': ['*']}

install_requires = \
['libcst>=0.4.7,<0.5.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['clean = printcleaner.clean:app']}

setup_kwargs = {
    'name': 'printcleaner',
    'version': '0.1.5',
    'description': 'The simplest way to remove print statements from your Python code',
    'long_description': "## Printcleaner: the simplest way to remove print statements from your Python code\n\n\n![GitHub](https://img.shields.io/github/license/larsvonschaff/printcleaner)\n![PyPI](https://img.shields.io/pypi/v/printcleaner)\n\n\nIs your Python code littered with random print statements from debugging or simply exploring?\n\nPrintcleaner is a simple CLI that removes all of them with one command. All you need to do is:\n\n\n**pip install printcleaner**\n\n**clean < name of your file or directory >**\n\nDone. Don't worry: comments, formatting, whitespace and everything else in your code will be preserved.\n\n",
    'author': 'A. L. Walker',
    'author_email': 'walkernotwalker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/leftfile/printcleaner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
