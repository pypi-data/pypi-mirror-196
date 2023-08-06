# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['allconnect', 'allconnect.allconnect', 'allconnect.tests']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.0,<3.0.0',
 'numpy>=1.22.2,<2.0.0',
 'replit>=3.2.4,<4.0.0',
 'urllib3>=1.26.12,<2.0.0']

setup_kwargs = {
    'name': 'allconnect',
    'version': '0.1.0',
    'description': 'Este é um pacote Python que oferece integrações com várias plataformas de comunicação, incluindo Discord, Telegram e WhatsApp, com a promessa de incluir mais integrações no futuro. Com ele, você pode enviar e receber mensagens, bem como realizar outras operações relacionadas à comunicação, usando essas plataformas. Este pacote é atualizável e estará em constante evolução para fornecer suporte para as plataformas mais populares ',
    'long_description': None,
    'author': 'darkslwlinc',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<3.11',
}


setup(**setup_kwargs)
