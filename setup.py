#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os.path


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
        'tg_utils.health_check',
        'tg_utils.health_check.checks',
        'tg_utils.health_check.checks.phantomjs',
        'tg_utils.health_check.checks.elvis',
        'tg_utils.health_check.checks.celery_beat',
    ],
    package_dir={
        'tg_utils': 'tg_utils',
        'tg_utils.health_check': os.path.join('tg_utils', 'health_check'),
        'tg_utils.health_check.checks': os.path.join('tg_utils', 'health_check', 'checks'),
        'tg_utils.health_check.checks.phantomjs': os.path.join('tg_utils', 'health_check', 'checks', 'phantomjs'),
        'tg_utils.health_check.checks.elvis': os.path.join('tg_utils', 'health_check', 'checks', 'elvis'),
        'tg_utils.health_check.checks.celery_beat': os.path.join('tg_utils', 'health_check', 'checks', 'celery_beat'),
    },
    include_package_data=True,
    install_requires=[
        'django>=1.8,!=2.1.0,!=2.1.1,<3.0',
    ],
    extras_require={
        'lock': [
            'redis>=2.10.0',
            'python-redis-lock>=3.2.0,<4.0.0',
        ],
        'health_check': [
            'django-health-check>=3.9.0,<4.0.0',
            'psutil>=5.6.0,<6.0.0',
            'requests>=2.18.4,<3.0.0',
        ],
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
