#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='tap-netsuite-suite-sql',
    version='0.0.1',
    classifiers=['Programming Language :: Python :: 3 :: Only'],
    py_modules=['tap_netsuitesuiteql'],
    entry_points='''
        [console_scripts]
        tap-netsuitesuiteql=tap_netsnetsuitesuiteqluite:main
    ''',
    packages=find_packages(exclude=['tests']),
    package_data={
        'tap_netsuitesuiteql': ['schemas/*.json']
    },
    include_package_data=True,
)
