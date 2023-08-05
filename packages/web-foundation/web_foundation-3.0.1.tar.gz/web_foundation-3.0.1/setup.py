# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['web',
 'web.env',
 'web.env.database',
 'web.errors',
 'web.kernel',
 'web.kernel.messaging',
 'web.kernel.proc',
 'web.trend',
 'web.trend.grpc',
 'web.trend.rest',
 'web.trend.rest.utils',
 'web.utils']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0']

extras_require = \
{'database': ['tortoise-orm[asyncpg]>=0.19.3,<0.20.0'],
 'grpc': ['betterproto[compiler]==2.0.0b4', 'grpcio-tools>=1.51.3,<2.0.0'],
 'rest': ['pydantic>=1.10.5,<2.0.0',
          'sanic>=22.12.0,<23.0.0',
          'orjson>=3.8.6,<4.0.0',
          'sanic-ext>=22.12.0,<23.0.0'],
 'shcheduler': ['apscheduler>=3.10.0,<4.0.0']}

entry_points = \
{'console_scripts': ['fix-proto = pip install Jinja2==3.1.2']}

setup_kwargs = {
    'name': 'web-foundation',
    'version': '3.0.1',
    'description': 'python web-server template',
    'long_description': '',
    'author': 'yaroher',
    'author_email': 'yaroher2442@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
