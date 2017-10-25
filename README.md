# iptables_converter  [![Build Status](https://travis-ci.org/sl0/conv.svg?branch=master)](https://travis-ci.org/sl0/conv)

**iptables_converter**:
    convert iptables to iptables-save format, output comes with [0:0] for iptables-restore -c

**ip6tables_converter**:
   convert ip6tables to ip6tables-save format, output comes with [0:0] for ip6tables-restore -c

**Licenses**: 

  1. GPLv3, or any newer version, see LICENSE.txt
  1. Apache License version 2, see LICENSE_APACHE.txt

Author:  Johannes Hubertz   <johannes@hubertz.de>

Version: 0.9.9

Date:    2017-10-25


**iptables_converter** speeds up loading of iptables-commands by converting
them to iptables-save format and then loading them through iptables-restore.

Usage:

    iptables_converter [ -s source ] [ --sloppy ]

This assumes that **source** is a plain ascii-file containing lines starting with
iptables to build a firewall ruleset.  Lines starting with **/sbin/iptables** are
understood as well.  Omitting -s source defaults to reading a file named **rules**.
An optional **sloppy** parameter makes premature definitions (-N name) of any user
defined chains unneccessary, they are defined automatically by first mentioning
them.
Output to stdout gives a maximum of flexibility. Packet-counters and
byte-counters include [0:0] which keeps compatibility to iptables-restore as
well as to `iptables-restore -c`.

From version 0.9.10 on it works as a python-module using entry-points for easier 
imports. For your convienience, the module is named **iptables_conv** .

At travis-ci.org the **unittests** are run automatically, thanks to Guido!
To run them locally, please use python:

    python setup test

It is tested to work well with python2.7 and python3.5. Some sphinx
documentation is prepared.
Debian packages are provided for the [binaries][1] and
[sphinx-documentation][2]. git-buildpackage creates them on the fly. RPMs may
be created by python `setup.py bdist_rpm`.

Any comments welcome.

Have fun!

Johannes


[![Build Status](https://travis-ci.org/sl0/conv.svg?branch=master)](https://travis-ci.org/sl0/conv)

[1]: https://packages.debian.org/sid/iptables-converter
[2]: https://packages.debian.org/sid/iptables-converter-doc

