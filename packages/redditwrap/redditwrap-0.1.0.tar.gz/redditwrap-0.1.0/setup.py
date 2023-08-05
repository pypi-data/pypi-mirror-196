# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['redditwrap']
setup_kwargs = {
    'name': 'redditwrap',
    'version': '0.1.0',
    'description': "It's 'RedditWarp' not 'RedditWrap'.",
    'long_description': 'None',
    'author': 'Pyprohly',
    'author_email': 'pyprohly@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
}


setup(**setup_kwargs)
