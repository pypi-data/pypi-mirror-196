#!/usr/bin/env python

from io import open
from setuptools import setup


version = '0.0.16'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='transQA',
    version=version,

    author='KovrizhnykhDY',
    author_email='kovrizhnykhdyu@consultant.ru',

    description=(
        u'Lib for transformer NN question answering'

    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['transQA'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
