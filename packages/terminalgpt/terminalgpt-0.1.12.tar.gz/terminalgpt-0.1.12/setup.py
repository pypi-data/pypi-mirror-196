# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terminalgpt']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'colorama>=0.4.6,<0.5.0',
 'cryptography>=39.0.2,<40.0.0',
 'openai>=0.27.0,<0.28.0',
 'tiktoken>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['terminalgpt = terminalgpt.main:cli']}

setup_kwargs = {
    'name': 'terminalgpt',
    'version': '0.1.12',
    'description': 'AI chat asistent in your terminal powered by OpenAI GPT-3.5',
    'long_description': "# TerminalGPT\n\nWelcome to terminalGPT, the terminal-based ChatGPT personal assistant app! With terminalGPT, you can easily interact with ChatGPT and receive short, easy-to-read answers on your terminal.\n\nterminalGPT is specifically optimized for your machine's operating system, distribution, and chip set architecture, so you can be sure that the information and assistance you receive are tailored to your specific setup.\n\nWhether you need help with a quick question or want to explore a complex topic, TerminalGPT is here to assist you. Simply enter your query and TerminalGPT will provide you with the best answer possible based on its extensive knowledge base.\n\nThank you for using TerminalGPT, and we hope you find the terminal-based app to be a valuable resource for your day-to-day needs!\n\n## Pre-requisites\n\n1. Python 3.9 or higher\n2. [An OpenAI Account and API key](https://elephas.app/blog/how-to-create-openai-api-keys-cl5c4f21d281431po7k8fgyol0) that you can get for free with a limited quota.\n\n## Installation\n\n1. Install the package with pip install.\n\n```sh\nterminalgpt install\n```\n\n2. Enter your OpenAI API key when prompted and press enter\n\nThat's it! You're ready to use TerminalGPT!\n\n---\n\n## Usage\n\n1. Run the program with the following command:\n\n```sh\nterminalgpt\n```\n\n## Illustration\n\n![Alt Text](./usage.gif)\n",
    'author': 'Adam Yodinsky',
    'author_email': '27074934+adamyodinsky@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
