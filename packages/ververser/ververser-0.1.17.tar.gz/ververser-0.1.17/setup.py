# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ververser',
 'ververser.examples.1_minimal_setup',
 'ververser.examples.1_minimal_setup.content',
 'ververser.examples.2_game_class',
 'ververser.examples.2_game_class.content',
 'ververser.examples.3_global_reinitialisation',
 'ververser.examples.3_global_reinitialisation.content',
 'ververser.examples.4_local_reinitialisation',
 'ververser.examples.4_local_reinitialisation.content',
 'ververser.examples.5_mouse_and_keyboard',
 'ververser.examples.5_mouse_and_keyboard.content']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.2,<2.0.0', 'pyglet>=2.0.5,<3.0.0']

setup_kwargs = {
    'name': 'ververser',
    'version': '0.1.17',
    'description': 'A lightweight wrapper around pyglet that allows hot-reloading of content.',
    'long_description': 'None',
    'author': 'Berry van Someren',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
