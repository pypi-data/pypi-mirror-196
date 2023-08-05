# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slurm_script']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['slurm_script = slurm_script.main:main']}

setup_kwargs = {
    'name': 'slurm-script',
    'version': '0.1.1',
    'description': 'Python Slurm script interface',
    'long_description': '# `slurm_script` Python Slurm command generator\n\nThis package is designed to generate slurm script to submit `mpi` jobs to a cluster.\n',
    'author': 'Kyoungseoun Chung',
    'author_email': 'kyoungseoun.chung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
