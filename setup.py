""" setup.py for iptables-converter
"""

import os
import sys
import iptables_conv

from setuptools import setup, find_packages


if sys.argv[-1] == 'test':
    dev_requirements = [
        'pytest',
        'flake8',
        'coverage'
    ]
    try:
        _ = map(__import__, dev_requirements)
    except ImportError as err:
        err_msg = err.message.replace("No module named ", "")
        msg = "%s is not installed. Install your test requirments." % err_msg
        raise ImportError(msg)
    os.system('flake8 iptables_conv tests')
    os.system('py.test')
    sys.exit()


setup(name='iptables-converter',
      description='convert set of iptables-commands to iptables-save format',
      long_description=open('README.rst').read(),
      version=iptables_conv.__version__,
      license=iptables_conv.__license__,
      author=iptables_conv.__author__,
      author_email=iptables_conv.__author_email__,
      url=iptables_conv.__url__,
      platforms=['Linux', ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: '
          'GNU General Public License v3 or later (GPLv3+)',
          'License :: OSI Approved :: Apache Software License',
          'Intended Audience :: System Administrators',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: Security',
          'Topic :: System :: Networking :: Firewalls',
          'Topic :: Utilities',
      ],
      packages=find_packages(exclude=['tests', ]),
      entry_points={
          'console_scripts': [
              'iptables-converter=iptables_conv.iptables_converter:main',
              'ip6tables-converter=iptables_conv.iptables_converter:main',
          ],
      },
     )
