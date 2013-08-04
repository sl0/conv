# ################################################################### #
#                                                                     #
#       README.txt for iptables_converter.py                          #
#                                                                     #
#       iptables_converter.py:                                        #
#                convert iptables to iptables-save format             #
#                output comes with [0:0] for iptables-restore -c      #
#       License: GPLv3, or any newer version                          #
#                see LICENSE.txt                                      #
#                                                                     #
#       Author:  Johannes Hubertz   <johannes@hubertz.de>             #
#       Version: 0.9                                                  #
#       Date:    2013-08-05                                           #
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
        iptables_converter.py [ -s source ]

        which assumes, source is a plain ascii-file containing
        lines starting with iptables to build a firewall ruleset
        lines starting with /sbin/iptables are understood as well
        ommitting -s source defaults to read a file named: rules

        output is stdout to give a maximum of flexibility
        paket-countes and byte-counters included now: [0:0]
        which keeps compatiblity to iptables-restore as well as to
        iptables-restore -c

        Tests have been written using unittests, see file:
        iptables_converter_tests.py, test coverage 92%,
        untested: main and optparse, but they seem to be OK ;-)

        Comments welcome
# ################################################################### #
# EoF
