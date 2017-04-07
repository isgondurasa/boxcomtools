#!/usr/bin/env python

from setuptools import setup

install_requires = (
    'aiohttp >= 1.3.3',
    'aiohttp-jinja2 >= 0.13.0',
    'async-timeout >= 1.1.0',
)

tests_require = (
    'py == 1.4.32',
    'pytest >= 3.0.6',
    'pytest-aiohttp >= 0.1.3',
    'pytest-cov >= 2.4.0',
    'pytest-env >= 0.6.0',
    'coverage >= 4.3.4'
)

setup(name='boxcomtools',
      version='0.0.8',
      description='A set of tools to transfer data between box and smartsheet',
      license='Apache License 2.0',
      author='Andrey Sviridov',
      author_email='isgondurasa@gmail.com',
      url='https://github.com/isgondurasa/boxcomtools',
      packages=['boxcomtools'],
      install_requires=install_requires,
      tests_require=tests_require
     )
