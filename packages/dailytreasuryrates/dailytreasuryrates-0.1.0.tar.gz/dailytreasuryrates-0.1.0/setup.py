# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['dailytreasuryrates']
install_requires = \
['argparse>=1.1.0,<2.0.0', 'pandas>=1.1.2,<2.0.0']

entry_points = \
{'console_scripts': ['dailytreasuryrates = dailytreasuryrates:cli']}

setup_kwargs = {
    'name': 'dailytreasuryrates',
    'version': '0.1.0',
    'description': 'Daily Treasury Rates Downloader',
    'long_description': '# dailytreasuryrates\nDaily Treasure Rate Downloader\n',
    'author': 'Thijs van den Berg',
    'author_email': 'thijs@sitmo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
