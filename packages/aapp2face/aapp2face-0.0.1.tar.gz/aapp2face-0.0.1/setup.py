# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['demo']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.7.0,<0.8.0', 'zeep>=4.2.1,<5.0.0']

entry_points = \
{'console_scripts': ['demo = demo.main:app']}

setup_kwargs = {
    'name': 'aapp2face',
    'version': '0.0.1',
    'description': 'A demo package of an application to obtain the capital of a country using a SOAP web service.',
    'long_description': '# Demo\n\nA demo package of an application to obtain the capital of a country using a SOAP web service.\n\n---\n\nDocumentación: [https://antmartinez68.github.io/demo](https://antmartinez68.github.io/demo)\n\nCódigo fuente: [https://github.com/antmartinez68/demo](https://github.com/antmartinez68/demo)\n\n---\n\nUso:\n\n```console\n$ demo IT\nThe capital of Italy is Rome\nDemo with love 💜\n\n```\n\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
