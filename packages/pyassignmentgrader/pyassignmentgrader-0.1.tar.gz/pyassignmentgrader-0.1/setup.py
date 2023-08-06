# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyassignmentgrader']

package_data = \
{'': ['*']}

install_requires = \
['fspathtree>=0.8,<0.9',
 'pytest-pudb>=0.7.0,<0.8.0',
 'pytest>=7.2.2,<8.0.0',
 'pyyaml>=6.0,<7.0',
 'typer[all]==0.1']

entry_points = \
{'console_scripts': ['pygrader = pyassignmentgrader.cli:app']}

setup_kwargs = {
    'name': 'pyassignmentgrader',
    'version': '0.1',
    'description': '',
    'long_description': '# pyAssignmentGrader\n\nA Python module and command-line utility for grading assignments. This tool was\ndeveloped to grade assignments for my Phys 312 : Scientific Computing and Productivity\nclass at Fort Hays State University.\n\nCurrently it is only being developed to suit my specific needs.\n',
    'author': 'CD Clark III',
    'author_email': 'clifton.clark@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
