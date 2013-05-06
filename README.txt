# ################################################################### #
#                                                                     #
#                                                                     #
#       README.txt for conv.py                                        #
#                                                                     #
#       conv.py: convert iptables to iptables-save format             #
#                output comes with [0:0] for iptables-restore -c      #
#       License: GPLv3, or any newer version                          #
#                see LICENSE.txt                                      #
#                                                                     #
#       Author:  sl0            <sl0.self@googlemail.com>             #
#       Version: 0.4                                                  #
#       Date:    2013-05-05                                           #
#                                                                     #
#       Details: have a look into the tests, please                   #
#       Comments welcome                                              #
#       Have fun!                                                     #
#                                                                     #
# ################################################################### #


conv.py
=======

conv.py:    speeds up loading of many iptables-commands
            by converting to iptables-save format

    Usage:
        conv.py -s source 

        this assumes, source is a plain ascii-file containing
        lines starting with iptables to build a firewall ruleset
        
        output is stdout to give a maximum of flexibility
        paket-countes and byte-counters included now: [0:0]
        this is compatible to:
        iptables-restore as well as to iptables-restore -c

        Tests ave been written using unittests, see conv_tests.py
        test coverage 88%, 
        not tested: main and optparse, but they seem to be OK ;-)

# ################################################################### #
# EoF
