#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from tg_utils import __version__ as version


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


setup(
    name='tg-utils',
    version=version,
    description="Common utils for Django-based projects.",
    long_description=readme + '\n\n' + history,
    author="Thorgate",
    author_email='code@thorgate.eu',
    url='https://github.com/thorgate/tg-utils',
    packages=[
        'tg_utils',
    ],
    package_dir={'tg_utils':
                 'tg_utils'},
    include_package_data=True,
    install_requires=[
        'django>=1.8,!=2.1.0,!=2.1.1,<2.2',
    ],
    extras_require={
        'lock': [
            'python-redis-lock>=3.2.0',
        ]
    },
    license="ISCL",
    zip_safe=False,
    keywords='tg-utils tg_utils',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
