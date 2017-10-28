import sys
from setuptools import setup, find_packages


setup(name='iptables-converter',
      description='convert set of iptables-commands to iptables-save format',
      long_description=open('README.md').read(),
      version='0.9.10',
      license='GNU General Public License version 3 (or later)',
      platforms=['Linux', ],
      author='Johannes Hubertz',
      author_email='johannes@hubertz.de',
      url='https://github.com/sl0/conv.git',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
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
            'iptables_converter=iptables_conv.iptables_converter:main',
            'ip6tables_converter=iptables_conv.iptables_converter:main',
        ],
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      )
