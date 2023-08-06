# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['crappackage']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['crappackage = crappackage.unhelpful:main']}

setup_kwargs = {
    'name': 'crappackage',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Crappackage\n\nA garbage package to try stuff out on pypi\n\n## Installation\n\n`python3 -m pip install crappackage`\n',
    'author': 'alexrembridge',
    'author_email': 'a.rembridge@hotmail.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
