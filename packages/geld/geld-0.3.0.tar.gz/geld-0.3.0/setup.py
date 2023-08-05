# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geld', 'geld.common', 'geld.sync']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'geld',
    'version': '0.3.0',
    'description': 'A library to handle money operations',
    'long_description': '# Geld\n\nA library to easily handle currency conversions.\n\n\n## Official documentation\n- We do not have an official documentation yet, we are working on this.\n\n## Data origin\nCurrently the API used to get the values is https://theforexapi.com/api. (If the forex API the default client will not work)\nWe are working to make the lib extensable so you can pick info from different sources in the future.\n\n\n## How to install\n\n```\npip install geld\n```\n\n## How to use the Sync Client\n\nCode:\n```python\nfrom geld.clients import sync_client as client\nresult = client.convert_currency("USD", "BRL", 25, "2021-12-05")\nprint(result)\n```\n\nResult:\n```\n141.0127535205030424592109739\n```',
    'author': 'Affonso Brian Pereira Azevedo',
    'author_email': 'contato.affonsobrian@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/affonsobrian/geld',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
