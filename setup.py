#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='skame',
    version=":versiontools:skame:",
    description="Schema validation for python dicts",
    long_description="",
    keywords='schema, validation',
    author='Anler Hernandez Peral, Jesús Espino García',
    author_email='anler86@gmail.com, jespinog@gmail.com',
    url='https://github.com/kaleidos/skame',
    license='BSD',
    packages=['skame'],
    install_requires=[],
    setup_requires=[
        'versiontools >= 1.9.1',
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
