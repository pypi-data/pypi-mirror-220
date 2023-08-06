# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dai_python_commons']

package_data = \
{'': ['*']}

install_requires = \
['boto3-stubs[glue,s3]>=1.26.0,<2.0.0',
 'boto3>=1.26.0,<2.0.0',
 'loguru>=0.7.0,<0.8.0']

extras_require = \
{'data-consolidation': ['pyarrow==12.0.0',
                        's3fs==2023.6.0',
                        'aiobotocore==2.5.2'],
 'glue': ['awswrangler==3.2.1', 'cryptography==41.0.2']}

setup_kwargs = {
    'name': 'dai-python-commons',
    'version': '5.0.0',
    'description': 'Collection of small python utilities useful for lambda functions or glue jobs. By the Stockholm Public Transport Administration.',
    'long_description': 'None',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.11,<3.12',
}


setup(**setup_kwargs)
