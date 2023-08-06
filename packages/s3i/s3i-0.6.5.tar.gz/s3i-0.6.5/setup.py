# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3i']

package_data = \
{'': ['*']}

install_requires = \
['alabaster>=0.7.12',
 'astroid>=2.3.3',
 'asyncio>=3.4.3,<4.0.0',
 'certifi>=2019.11.28',
 'cffi>=1.13.2',
 'chardet>=1.13.2',
 'colorama>=0.4.3',
 'cryptography==3.1',
 'idna>=2.8',
 'jinja2<3.1',
 'jsonschema>=3.2.0',
 'lazy-object-proxy>=1.4.3',
 'markupsafe>=1.1.1',
 'mccabe>=0.6.1',
 'pgpy>=0.5.4,<0.6.0',
 'pika>=1.2.0',
 'pockets>=0.9.1',
 'pycparser>=2.19',
 'pygments>=2.5.2',
 'pyjwt==1.6.1',
 'pynput>=1.7.6,<2.0.0',
 'pyparsing>=2.4.5',
 'pyrql==0.7.0',
 'python-benedict>=0.21.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'python-gnupg>=0.5.0,<0.6.0',
 'requests>=2.26.0',
 'schema>=0.7.1',
 'six>=1.13.0',
 'snowballstemmer>=2.0.0',
 'typed-ast>=1.4.0',
 'urllib3>=1.25.7',
 'uuid>=1.30,<2.0',
 'websocket-client>=1.4.1,<2.0.0',
 'wrapt>=1.11.2']

setup_kwargs = {
    'name': 's3i',
    'version': '0.6.5',
    'description': 'S3I Basic functions',
    'long_description': '# Documentation\nThis package contains everything you need to get started with the S3I. The documentation of the S3I package and its demos can be found [here](https://kwh40.pages.rwth-aachen.de/s3i/).\n\n# Installation\ns3i is available on PyPI:\n\n```\npython -m pip install s3i\n```\n\n# Development\nThe s3i source code is hosted on [gitlab](https://git.rwth-aachen.de/kwh40/s3i). \n\n## Contributing\nFeel free to contribute to this project. For more details on submitting changes see [CONTRIBUTING.md](./CONTRIBUTING.md)',
    'author': 'Kompetenzzentrum Wald und Holz 4.0',
    'author_email': 's3i@kwh40.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://kwh40.pages.rwth-aachen.de/s3i/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
