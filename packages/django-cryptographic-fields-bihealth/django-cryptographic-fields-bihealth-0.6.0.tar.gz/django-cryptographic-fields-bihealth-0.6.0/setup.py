#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-cryptographic-fields-bihealth',
    version="0.6.0",
    packages=find_packages(),
    license='MIT',
    include_package_data=True,
    description=(
        'A set of django fields that internally are encrypted using the '
        'cryptography.io native python encryption library.'
    ),
    url='http://github.com/bihealth/django-cryptographic-fields/',
    author='Manuel Holtgrewe, Mikko Nieminen, Oliver Stolpe',
    author_email='manuel.holtgrewe@bih-charite.de, mikko.nieminen@bih-charite.de, oliver.stolpe@bih-charite.de',
    install_requires=[
        'Django>=3.0',
        'cryptography>=0.8.2',
    ],
    keywords=['encryption', 'django', 'fields', ],
)
