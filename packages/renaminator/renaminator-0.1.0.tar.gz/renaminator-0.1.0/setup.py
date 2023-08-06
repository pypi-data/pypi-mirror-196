# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['renaminator']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['renaminator = renaminator.__main__:main']}

setup_kwargs = {
    'name': 'renaminator',
    'version': '0.1.0',
    'description': 'A file renaming utility',
    'long_description': '# Renaminator\n\nThe idea is to have a simple way to remove a string from a bunch of files in a directory.\n\n### Roadmap \n- [ ] Print result\n- [ ] Add error/exception handling\n- [ ] Add GUI',
    'author': 'Tsierenana Bôtramanagna Gracy',
    'author_email': 'gtsierenana@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
