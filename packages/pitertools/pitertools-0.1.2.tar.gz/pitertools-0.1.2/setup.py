# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pitertools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pitertools',
    'version': '0.1.2',
    'description': '',
    'long_description': '# pitertools\nTools to process python iterators in parallel.\n\n## map_parallel\nSpin up n threads to pull from input iterator and run an operation on it in parallel\n\n##\nRoadmap\n- Add more tests \n- Add some linter, static type checking\n- Add `ordered` parameter to `map_parallel` (currently results are unordered)\n- Allow running on external executor\n',
    'author': 'tsah',
    'author_email': 'tsah.weiss@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tsah/pitertools',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
