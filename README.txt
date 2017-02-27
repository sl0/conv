# ################################################################### #
#                                                                     #
#       README.txt for iptables_converter.py                          #
#                  and ip6tables_converter.py                         #
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


iptables_converter.py
=====================

iptables_converter.py:
        speeds up loading of many iptables-commands
        by converting to iptables-save format and then
        loading through iptables-restore

    Usage:
        iptables_converter.py [ -s source ] [ --sloppy ]

        which assumes, source is a plain ascii-file containing
        lines starting with iptables to build a firewall ruleset
        lines starting with /sbin/iptables are understood as well
        omitting -s source defaults to read a file named: rules

        An optional sloppy parameter makes premature definitions
        of any user defined chains unneccessary, they are defined
        automatically by first mentioning.

        output to stdout gives a maximum of flexibility
        packet-counters and byte-counters included now: [0:0]
        which keeps compatibility to iptables-restore as well as to
        iptables-restore -c

        Tests have been written using unittests, see file:
        iptables_converter_tests.py.

        It is tested to work well with python2.7 and
        python3.5. Some sphinx documentation is prepared.

        Debian packages shipped for binary and sphinx-documentation
        git-buildpackage creates them on the fly.
        RPMs may be created by python setup.py bdist_rpm

        Any Comments welcome.
        Have fun!
        Johannes
# ################################################################### #
# EoF
