# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cdk_proxy_api_client',
 'cdk_proxy_api_client.common',
 'cdk_proxy_api_client.models']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'cdk-proxy-api-client',
    'version': '0.1.0',
    'description': 'Conduktor Proxy API Client',
    'long_description': '# cdk-proxy-api-client\n\nAPI Client library to interact with Conduktor Proxy\n\nCurrent version: v1beta1\n\n\n## Features\n\n* Create new Token for a tenant\n* List all topic mappings for a tenant\n* Create a new mapping for a tenant\n* Delete a tenant - topic mapping\n* Delete all topic mappings for a tenant\n',
    'author': 'John "Preston" Mille',
    'author_email': 'john@ews-network.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
