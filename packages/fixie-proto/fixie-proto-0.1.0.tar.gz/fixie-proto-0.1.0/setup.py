# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python']

package_data = \
{'': ['*']}

install_requires = \
['protobuf>=4.23.4,<5.0.0']

setup_kwargs = {
    'name': 'fixie-proto',
    'version': '0.1.0',
    'description': '',
    'long_description': '# fixie-proto\nRepository containing protos. The intention is for this to define our public-facing APIs. Tooling in this repository should then make it easy to use the *already compiled* protos in various languages.\n\nFor languages supported by the Buf Schema Registry, instructions for adding these protos like a normal dependency can be found [here](https://buf.build/fixie-ai/fixie/assets/main).  For example, to add a TypeScript dependency using yarn:\n\n```\nyarn config set npmScopes.buf.npmRegistryServer https://buf.build/gen/npm/v1/\nyarn add @buf/fixie-ai_fixie.bufbuild_connect-es@latest\n```\n\nWe also support additional languages (albeit with fewer options) directly. In particular, Python is available via pip: [PyPI]().\n',
    'author': 'Fixie.ai Team',
    'author_email': 'founders@fixie.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
