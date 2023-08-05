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
    'version': '0.1.8',
    'description': 'Python Slurm script interface',
    'long_description': '# `slurm_script` Python Slurm command generator\n\nThis package is designed to generate slurm script to submit `mpi` jobs to a cluster.\n\n## Installation\n\nYou can install the package using `pip`.\n\n```bash\npython -m pip install slurm_script\n```\n\n## Usage\n\n```bash\n$ sjob --h\nslurm_script version: 0.1.7\nusage: slurm_script/sjob [-h] [-n NPROC] [-j JOB_NAME] [-t TIME] [-m MEM_PER_CPU] [-c COMMAND [COMMAND ...]] [-mail MAIL_TYPE]\n                         [-nt NTASKS] [-cnt CPUS_PER_TASK] [-a ADDITIONAL_CMD [ADDITIONAL_CMD ...]]\n\npython interface to generate and run slurm command.\n\noptions:\n  -h, --help            show this help message and exit\n  -n NPROC, --nproc NPROC\n                        Number of processors to run the job.\n  -j JOB_NAME, --job_name JOB_NAME\n                        Name of the job.\n  -t TIME, --time TIME  Maximum runtime [hours:minutes:second].\n  -m MEM_PER_CPU, --mem_per_cpu MEM_PER_CPU\n                        Memory per core [MB].\n  -c COMMAND [COMMAND ...], --command COMMAND [COMMAND ...]\n                        Program command.\n  -mail MAIL_TYPE, --mail_type MAIL_TYPE\n                        Email notification at either BEGIN, END, or FAIL.\n  -nt NTASKS, --ntasks NTASKS\n                        Number of tasks.\n  -cnt CPUS_PER_TASK, --cpus_per_task CPUS_PER_TASK\n                        Number of cpus per task.\n  -a ADDITIONAL_CMD [ADDITIONAL_CMD ...], --additional_cmd ADDITIONAL_CMD [ADDITIONAL_CMD ...]\n                        Additional commands.\n```\n\n## Note\n\nIt seems like due to a security reason, it is not possible to use `sjob` command directly from the cluster.\nTherefore, you can use the following command instead\n\n```bash\npython -m slurm_script --h\n```\n\n## Example\n\n```bash\n$ sjob -n 10 -j test_run -t 10:00:00 -m 1024 -mail BEGIN,END,FAIL -nt 1 -cnt 10 -a module add python -c python test.py\nslurm_script version: 0.1.6\n\nPreview of the generated script:\n--------------------------------\n#!/bin/bash\n\n#SBATCH -n 10\n#SBATCH --job-name=test_run\n#SBATCH --time=10:00:00\n#SBATCH --mem-per-cpu=1024\n#SBATCH --mail-type=BEGIN,END,FAIL\n#SBATCH --ntasks=1\n#SBATCH --cpus-per-task=10\n\nmodule add python\n\nmpirun python test.py\n--------------------------------\nDo you want to run the script? [y/n] \n```\n',
    'author': 'Kyoungseoun Chung',
    'author_email': 'kyoungseoun.chung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
