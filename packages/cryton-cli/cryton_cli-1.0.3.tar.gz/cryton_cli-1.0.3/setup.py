# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cryton_cli',
 'cryton_cli.etc',
 'cryton_cli.lib',
 'cryton_cli.lib.commands',
 'cryton_cli.lib.util']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'PyYAML>=6.0.1,<7.0.0',
 'click>=8.1.2,<9.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'python-dotenv>=1.0.0,<2.0.0',
 'pytz>=2022.7,<2023.0',
 'requests>=2.27.0,<3.0.0',
 'termcolor>=2.2.0,<3.0.0',
 'tzlocal>=4.1,<5.0']

entry_points = \
{'console_scripts': ['cryton-cli = cryton_cli.lib.cli:cli']}

setup_kwargs = {
    'name': 'cryton-cli',
    'version': '1.0.3',
    'description': 'Command line interface for Cryton Core',
    'long_description': '![Coverage](https://gitlab.ics.muni.cz/cryton/cryton-cli/badges/master/coverage.svg)\n\n[//]: # (TODO: add badges for python versions, black, pylint, flake8, unit tests, integration tests)\n\n# Cryton CLI\nCryton CLI is a command line interface used to interact with [Cryton Core](https://gitlab.ics.muni.cz/cryton/cryton-core) (its API).\n\nCryton toolset is tested and targeted primarily on **Debian** and **Kali Linux**. Please keep in mind that **only \nthe latest version is supported** and issues regarding different OS or distributions may **not** be resolved.\n\nFor more information see the [documentation](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/components/cli/).\n\n## Quick-start\nPlease keep in mind that [Cryton Core](https://gitlab.ics.muni.cz/cryton/cryton-core) must be running and its REST API must be reachable.\n\nMake sure [Docker](https://docs.docker.com/engine/install/) is installed.\nOptionally, check out these Docker [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/).\n\nThe following script starts an interactive shell using Docker. \n```shell\ndocker run -it --network host registry.gitlab.ics.muni.cz:443/cryton/cryton-cli\n```\n\nUse the following to invoke the app:\n```shell\ncryton-cli\n```\n\nFor more information see the [documentation](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/components/cli/).\n\n## Contributing\nContributions are welcome. Please **contribute to the [project mirror](https://gitlab.com/cryton-toolset/cryton-cli)** on gitlab.com.\nFor more information see the [contribution page](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/latest/contribution-guide/).\n',
    'author': 'Ivo Nutár',
    'author_email': 'nutar@ics.muni.cz',
    'maintainer': 'Jiří Rája',
    'maintainer_email': 'raja@ics.muni.cz',
    'url': 'https://gitlab.ics.muni.cz/cryton',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
