.. image:: https://travis-ci.org/sl0/conv.svg?branch=master
    :target: https://travis-ci.org/sl0/conv
    :align: right

iptables-converter
==================


**iptables-converter**: convert iptables to iptables-save format, output
comes with [0:0] for iptables-restore -c

**ip6tables-converter**: convert ip6tables to ip6tables-save format,
output comes with [0:0] for ip6tables-restore -c

**Source**: https://github.com:sl0/conv.git

**Version**: 0.9.10.rc1

**Date**: 2017-11-08

**Licenses**:

    - GNU GENERAL PUBLIC LICENSE Version 3 later
    - Apache License Version 2.0

**Author**: Johannes Hubertz johannes@hubertz.de

**iptables-converter** speeds up loading of iptables-commands by
converting them to iptables-save format, and then loading them through
iptables-restore is much more quicker than loading the plain commands.
The loading itself is not part of iptables-converter.

Usage:

::

    iptables-converter [ -d destination ] [ -s source ] [ --sloppy ]
    ip6tables-converter [ -d destination ] [ -s source ] [ --sloppy ]

This assumes that **source** is a plain ascii-file containing lines
starting with **iptables** to build a firewall ruleset. Lines starting
with **/sbin/iptables** are understood as well. Omitting -s source
defaults to reading a file named **rules**. An optional **sloppy**
parameter makes premature definitions (-N name) of any user defined
chains unneccessary, they are defined automatically by first mentioning
them. Optionally **-d destination** writes everything into the given
destination file since verstion 0.9.10. Omitting this option results in
writing Output to stdout, which is the default behavior. Packet-counters
and byte-counters include [0:0] which keeps compatibility to
iptables-restore as well as to **iptables-restore -c**.

**ip6tables-converter** works for ip6tables just the same way.

Both they work for **filter**, **mangle**, **nat** and **raw** tables,
**security** tables are not supported for now.

From version 0.9.10 on it works as a python-module using entry-points
for easier imports. For your convienience, the module is named
**iptables\_conv**.

At travis-ci.org the **tests** are run automatically, thanks to Guido!
To run them locally, please use python:

::

    python setup test

It is tested to work well with python2.7 and python3.5. The tests are
done using pytest for easier writing future testcases. Some sphinx
documentation is prepared. Debian packages are provided for the
`binaries <https://packages.debian.org/sid/iptables-converter>`__ and
`sphinx-documentation <https://packages.debian.org/sid/iptables-converter-doc>`__.
git-buildpackage creates them on the fly. RPMs may be created by python::

    setup.py bdist_rpm

Any comments welcome.

Have fun!

Johannes
