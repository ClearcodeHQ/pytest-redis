# -*- coding: utf-8 -*-
# Copyright (C) 2016 by Clearcode <http://clearcode.cc>
# and associates (see AUTHORS).

# This file is part of pytest-redis.

# pytest-redis is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pytest-redis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with pytest-redis. If not, see <http://www.gnu.org/licenses/>.
"""Installation module for pytest-redis."""

import os
from setuptools import setup, find_packages

here = os.path.dirname(__file__)


def read(fname):
    """
    Read given file's content.

    :param str fname: file name
    :returns: file contents
    :rtype: str
    """
    return open(os.path.join(here, fname)).read()


requirements = [
    'pytest>=3.0.0',
    'mirakuru>=0.2',  # test executors helpers
    'port-for>=0.3.1',  # needed for random port selection
    'redis'
]

test_requires = [
    'pytest-cov==2.4.0',
    'pytest-xdist==1.15.0',
    'Mock==2.0.0',
]

extras_require = {
    'tests': test_requires
}

setup(
    name='pytest-redis',
    version='1.2.0',
    description='Redis fixtures and fixture factories for Pytest.',
    long_description=(
        read('README.rst') + '\n\n' + read('CHANGES.rst')
    ),
    keywords='tests py.test pytest fixture redis',
    author='Clearcode - The A Room',
    author_email='thearoom@clearcode.cc',
    url='https://github.com/ClearcodeHQ/pytest-redis',
    license='LGPLv3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: '
        'GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=requirements,
    tests_require=test_requires,
    test_suite='tests',
    include_package_data=True,
    zip_safe=False,
    extras_require=extras_require,
    entry_points={
        'pytest11': [
            'pytest_redis = pytest_redis.plugin'
        ]},
)
