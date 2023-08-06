# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sahl_nutun_common']

package_data = \
{'': ['*'], 'sahl_nutun_common': ['z/*']}

install_requires = \
['attrs>=22.2.0,<23.0.0',
 'boto3>=1.26.89,<2.0.0',
 'httpx>=0.23.3,<0.24.0',
 'ptpython>=3.0.23,<4.0.0',
 'pyjwt>=2.6.0,<3.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'rich>=13.3.2,<14.0.0']

setup_kwargs = {
    'name': 'sahl-nutun-common',
    'version': '0.2.0',
    'description': 'Common modules for Nutun Authentifi interaction, including authenticated API calling',
    'long_description': 'None',
    'author': 'kimv',
    'author_email': 'kimv@sahomeloans.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
