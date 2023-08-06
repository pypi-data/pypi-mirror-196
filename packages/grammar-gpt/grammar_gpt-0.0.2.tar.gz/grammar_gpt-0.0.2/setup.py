# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grammar_gpt']

package_data = \
{'': ['*']}

install_requires = \
['revchatgpt>=3.3.4,<4.0.0']

setup_kwargs = {
    'name': 'grammar-gpt',
    'version': '0.0.2',
    'description': 'A simple grammar utility for everyone by using ChatGPT',
    'long_description': "# grammar-gpt\n\n\n\n\n\n# API\n```Python\n>>> from grammar_gpt import GrammarHelper\n>>> gh = GrammarHelper()\n>>> gh.polish('I am not like dance')\n'I do not like to dance.'\n\n\n>>> gh.translate('How are you doing')\n'你好吗？'\n>>> gh.translate('whats up')\n'最近怎么样？'\n\n```\n",
    'author': 'Xingyu Long',
    'author_email': 'dev.halolong@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
