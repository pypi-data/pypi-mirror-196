# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['replifactory',
 'replifactory.GUI',
 'replifactory.culture',
 'replifactory.device',
 'replifactory.status',
 'replifactory.test',
 'replifactory.util']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'ipython>=7.29.0,<8.0.0',
 'ipywidgets>=7.5.1,<8.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.3.0,<4.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.1.0,<2.0.0',
 'pyftdi>=0.52.9,<0.53.0',
 'schedule>=0.6.0,<0.7.0',
 'scipy>=1.6.3,<2.0.0']

setup_kwargs = {
    'name': 'replifactory',
    'version': '0.0.61',
    'description': 'replifactory morbidostat python package',
    'long_description': '',
    'author': 'Catalin Rusnac',
    'author_email': 'ctlnrsnc@gmail.com',
    'maintainer': 'Fedor Gagarin',
    'maintainer_email': 'fddgagarin@gmail.com',
    'url': 'https://replifactory.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
