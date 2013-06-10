#!/usr/bin/env python

import sys
from distutils.core import setup


setup(name='iptables-converter',
    description='convert set of iptables-commands to iptables-save format',
    long_description=open('README.txt').read(),
    version='0.6',
    license='GNU General Public License version 3 (or later)',
    platforms= ['Linux', ],
    author='sl0 (Johannes Hubertz)',
    author_email='sl0.self@googlemail.com',
    maintainer='sl0',
    maintainer_email='sl0.self@googlemail.com',
    url='https://github.com/sl0/conv.git',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Security',
        'Topic :: System :: Networking :: Firewalls',
        'Topic :: Utilities',
    ],
    py_modules=['iptables_converter', ],
    #'iptables_converter_tests'],
    )

