# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elf_py_utils',
 'elf_py_utils.CodeGen',
 'elf_py_utils.constants',
 'elf_py_utils.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'elf-py-utils',
    'version': '0.1.3.2',
    'description': '',
    'long_description': '',
    'author': 'TreeOfWord',
    'author_email': 'li_163jx@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
