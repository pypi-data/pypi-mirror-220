# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dikicli']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.0', 'requests>=2.25.1']

entry_points = \
{'console_scripts': ['diki = dikicli.cli:main']}

setup_kwargs = {
    'name': 'dikicli',
    'version': '0.5.0',
    'description': 'Commandline interface for diki.pl polish-english dictionary',
    'long_description': '# dikicli\n\nCommandline interface to diki.pl polish-english dictionary.\n\nDikicli allows you to use diki.pl from comfort of your terminal.\nAll results are cached for faster retrieval in the future.\n\n## Usage:\n\nTranslate english to polish:\n\n    diki word\n\nTranslate polish to engish:\n\n    diki -p word\n\nDisplay html file of all words translated so far:\n\n    diki -i\n\nShow usage statistics:\n\n    diki --stats\n',
    'author': 'Dawid Zych',
    'author_email': 'dwd@mailo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/silenc3r/dikicli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
