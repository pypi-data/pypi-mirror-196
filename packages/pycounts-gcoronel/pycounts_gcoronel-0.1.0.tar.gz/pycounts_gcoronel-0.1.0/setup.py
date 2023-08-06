# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycounts_gcoronel']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.3']

setup_kwargs = {
    'name': 'pycounts-gcoronel',
    'version': '0.1.0',
    'description': 'Calculate word counts in a text file as described in the Python Packages book!',
    'long_description': "# pycounts_gcoronel\n\nCalculate word counts in a text file as described in the Python Packages book!\n\n## Installation\nI haven't tried this way:\n```bash\n$ pip install pycounts_gcoronel\n```\nBut I tried this following the book:\n```bash\n$ conda activate pycounts_gcoronel\n```\nand then\n```bash\n$ poetry install\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pycounts_gcoronel` was created by Gabriel Coronel. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`pycounts_gcoronel` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n",
    'author': 'Gabriel Coronel',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
