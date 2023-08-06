# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['llama', 'llama.lemma', 'llama.lima']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'llama-and-llama',
    'version': '0.2.0',
    'description': 'LIMA',
    'long_description': '## llamas everywhere\n\nget some llamas @ https://pypi.org/project/llama-and-llama/\n\nwhat about llamas here? pip install llama-and-llama\n',
    'author': 'asdftoger',
    'author_email': 'asdftoger@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
