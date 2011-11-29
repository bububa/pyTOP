#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pyTOP

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup



if sys.argv[-1] == "register":
    os.system("python setup.py register")
    sys.exit()
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

if sys.argv[-1] == "test":
    os.system("python test.py")
    sys.exit()

required = []

if sys.version_info[:2] < (2,6):
    required.append('simplejson')

required.append('python-dateutil')
required.append('requests')

setup(
    name='pyTOP',
    version=pyTOP.__version__,
    description='Taobao Open Platform API Python Wrapper.',
    long_description=open('README.rst').read() + '\n\n' +
                     open('HISTORY.rst').read(),
    author='Syd Xu',
    author_email='prof.syd.xu@gmail.com',
    url='http://www.github.com/bububa/pyTOP',
    keywords = "taobao api wrapper TOP sdk",
    platforms="Python 1.5.0 and later.",
    packages= [
        'pyTOP',
        #'pyTOP.packages',
        #'pyTOP.packages.requests',
        #'pyTOP.packages.requests.packages.urllib3'
    ],
    install_requires=required,
    license='ISC',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Natural Language :: Chinese (Simplified)',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        # 'Programming Language :: Python :: 3.0',
        # 'Programming Language :: Python :: 3.1',
    ),
)
