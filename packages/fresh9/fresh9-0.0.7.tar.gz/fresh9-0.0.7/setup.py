#!/usr/bin/env python

from io import open
from setuptools import setup


version = '0.0.7'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fresh9',
    version=version,

    author='Dmitrii',
    author_email='refresher228@mail.ru',

    description=(
        u'Machinelearning hypr'

    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    packages=['fresh9'],
    
)
