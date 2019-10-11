#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from frp_runner import version

setup(
    name='frp_runner',
    version=version,
    url='https://github.com/wuyue92tree/frp_runner',
    description='frp manager',
    long_description=open('README.rst').read(),
    author='wuyue',
    author_email='wuyue92tree@163.com',
    maintainer='wuyue',
    maintainer_email='wuyue92tree@163.com',
    license='Apache License 2.0',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['frp_runner = frp_runner.manage:main']
    },
    install_requires=[
        'Django==2.2.6',
        'django-adminlte-ui==1.4.0'
    ],
)
