# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shimpy', 'shimpy.account', 'shimpy.address', 'shimpy.nft', 'shimpy.node']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.2.3,<2.0.0', 'click>=8.1.6,<9.0.0', 'iota-sdk==1.0.0rc1']

entry_points = \
{'console_scripts': ['shimpy = shimpy.cli:shimpy']}

setup_kwargs = {
    'name': 'shimpy',
    'version': '0.0.1',
    'description': 'Sample CLI Tool to interact with Shimmer Network.',
    'long_description': '# Shimpy\n\nSample CLI Tool to interact with Shimmer Network using [iota-sdk](https://pypi.org/project/iota-sdk/).\n\n## Install\n\n### Using pip\n\n`pip install shimpy`\n\n### Using poetry\n\n`poetry add shimpy`\n\n## Usage\n\n`shimpy --help`\n\n## Commands\n\n- info : Get Info about Node\n- account\n  - new: Generate new account\n  - balance: Get balance by account alias\n  - list: List all accounts\n- address\n  - new: Generate new address for account\n  - list: List all addresses in the account\n- nft\n  - mint: Mint new NFT\n  - send: Send NFT to an address\n\n### Contributions Welcome\n\n#### Under Development\n',
    'author': 'Kumar Anirudha',
    'author_email': 'mail@anirudha.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
