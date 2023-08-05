# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slurm_script']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['sjob = slurm_script.main:main']}

setup_kwargs = {
    'name': 'slurm-script',
    'version': '0.1.6',
    'description': 'Python Slurm script interface',
    'long_description': '# `slurm_script` Python Slurm command generator\n\nThis package is designed to generate slurm script to submit `mpi` jobs to a cluster.\n\n## Usage\n\n```bash\nslurm_script version: 0.1.2\nusage: slurm_script [-h] [-n NPROC] [-j JOB_NAME] [-t TIME] [-m MEM_PER_CPU]\n                    [-c COMMAND [COMMAND ...]]\n\npython interface to generate and run slurm command.\n\noptions:\n  -h, --help            show this help message and exit\n  -n NPROC, --nproc NPROC\n                        Number of processors to run the job.\n  -j JOB_NAME, --job-name JOB_NAME\n                        Name of the job.\n  -t TIME, --time TIME  Maximum runtime [hours:minutes:second].\n  -m MEM_PER_CPU, --mem-per-cpu MEM_PER_CPU\n                        Memory per core [MB].\n  -c COMMAND [COMMAND ...], --command COMMAND [COMMAND ...]\n                        Program command.\n```\n',
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
