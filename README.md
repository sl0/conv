```
# ################################################################### #
#                                                                     #
#       README.md for iptables_converter.py                           #
#                 and ip6tables_converter.py                          #
#                                                                     #
#       iptables_converter.py:                                        #
#                convert iptables to iptables-save format             #
#                output comes with [0:0] for iptables-restore -c      #
#       ip6tables_converter.py:                                       #
#                convert ip6tables to ip6tables-save format           #
#                output comes with [0:0] for ip6tables-restore -c     #
#       License: GPLv3, or any newer version                          #
#                see LICENSE.txt                                      #
#                                                                     #
#       Author:  Johannes Hubertz   <johannes@hubertz.de>             #
#       Version: 0.9.9                                                #
#       Date:    2017-02-27                                           #
#                                                                     #
#       Have fun!                                                     #
#                                                                     #
# ################################################################### #
```

iptables_converter.py
=====================

*iptables_converter.py* speeds up loading of iptables-commands by converting
them to iptables-save format and then loading them through iptables-restore.

Usage:

    iptables_converter.py [ -s source ] [ --sloppy ]

This assumes that *source* is a plain ascii-file containing lines starting with
iptables to build a firewall ruleset.  Lines starting with */sbin/iptables* are
understood as well.  Omitting -s source defaults to reading a file named
*rules*.

An optional sloppy parameter makes premature definitions of any user
defined chains unneccessary, they are defined automatically by first mentioning
them.

Output to stdout gives a maximum of flexibility.  Packet-counters and
byte-counters include [0:0] which keeps compatibility to iptables-restore as
well as to `iptables-restore -c`.

Tests have been written using unittests, see
*tests/test_iptables_converter.py*.

It is tested to work well with python2.7 and python3.5. Some sphinx
documentation is prepared.

Debian packages are provided for the [binaries][1] and
[sphinx-documentation][2]. git-buildpackage creates them on the fly.  RPMs may
be created by python `setup.py bdist_rpm`.

Any comments welcome.

Have fun!

Johannes

[1]: https://packages.debian.org/sid/iptables-converter
[2]: https://packages.debian.org/sid/iptables-converter-doc
```
# ################################################################### #
# EoF
```
