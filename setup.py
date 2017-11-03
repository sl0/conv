import os
import sys
from setuptools import setup, find_packages


if sys.argv[-1] == 'test':
    test_requirements = [
        'pytest',
        'flake8',
        'coverage'
    ]
    try:
        modules = map(__import__, test_requirements)
    except ImportError as err:
        err_msg = err.message.replace("No module named ", "")
        msg = "%s is not installed. Install your test requirments." % err_msg
        raise ImportError(msg)
    os.system('py.test')
    sys.exit()


setup(name='iptables-converter',
      description='convert set of iptables-commands to iptables-save format',
      long_description=open('README.md').read(),
      version='0.9.9.dev2',
      license='dual: GNU General Public License version 3 (or later), '
              'Apache Software License',
      platforms=['Linux', ],
      author='Johannes Hubertz',
      author_email='johannes@hubertz.de',
      url='https://github.com/sl0/conv.git',
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
      test_suite='nose.collector',
      tests_require=['nose'],
     )
