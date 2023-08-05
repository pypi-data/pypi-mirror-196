# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['natsu']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'natsu',
    'version': '1.0.0',
    'description': 'Use sum() with objects of any class',
    'long_description': '# natsu\n\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/natsu?logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/natsu)\n[![PyPI](https://img.shields.io/pypi/v/natsu?logo=pypi&color=green&logoColor=white&style=for-the-badge)](https://pypi.org/project/natsu)\n[![PyPI - License](https://img.shields.io/pypi/l/natsu?color=03cb98&style=for-the-badge)](https://github.com/celsiusnarhwal/natsu/blob/main/LICENSE.md)\n[![Code style: Black](https://aegis.celsiusnarhwal.dev/badge/black?style=for-the-badge)](https://github.com/psf/black)\n\nnatsu allows you to `sum()` Python objects of any class that implements `__add__()`.\n\n## Installation\n\n```bash\npip install natsu\n```\n\n## Usage\n\n```python\nfrom natsu import sum\n\nsum(some_iterable)\n```\n\n`natsu.sum()` is fully backwards-compatible with the built-in `sum()` function.\n\n## License\n\nnatsu is licensed under the [MIT License](LICENSE.md).\n',
    'author': 'celsius narhwal',
    'author_email': 'hello@celsiusnarhwal.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/celsiusnarhwal/natsu',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
