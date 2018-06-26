#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import os
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r'''^__version__ = ['"]([^'"]*)['"]''',
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)

    raise RuntimeError('Unable to find version string.')


long_description = read('README.md')

setup(
    name='iptv',
    version=find_version('iptv', '__init__.py'),
    description='IPTV database with a M3U playlist generator for LiveProxy.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/back-to/iptv',
    project_urls={
        'Documentation': 'https://back-to.github.io/',
        'Source': 'https://github.com/back-to/iptv/',
        'Tracker': 'https://github.com/back-to/iptv/issues',
    },
    author='back-to',
    author_email='backto@protonmail.ch',
    packages=['iptv'],
    entry_points={
        'console_scripts': [
            'iptv=iptv.main:main'
        ],
    },
    install_requires=[
        'fastjsonschema',
    ],
    python_requires='>=3.4, <4',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Video',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords='IPTV TV database channels streamlink liveproxy',
)
