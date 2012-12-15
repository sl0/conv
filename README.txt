# ################################################################### #
#                                                                     #
#                                                                     #
#       README.txt for conv.py                                        #
#                                                                     #
#       conv.py: convert iptables to iptables-save format             #
#                output comes with [0:0] for iptables-restore -c      #
#       License: GPLv3, see file gpl-3-0.txt                          #
#                                                                     #
#       Author:  sl0            <sl0.self@googlemail.com>             #
#       Date:    2012-12-15                                           #
#                                                                     #
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

# tests for object follow                                             #
#                                                                     #
#### Chains object ####################################################
# first test if object is loadable                     

   >>> #coding=utf-8
   >>> 
   >>> from conv import Chains, Tables
   >>>
   >>> dir()
   ['Chains', 'Tables', '__builtins__', '__name__', '__package__']
   >>>
   >>> filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])

# now we have an filtergroup object named filter
# lets see the structure of the empty object

   >>> dir()
   ['Chains', 'Tables', '__builtins__', '__name__', '__package__', 'filter']

   >>> filter.put_into_fgr("-P INPUT ACCEPT")
   >>> print filter
   {'FORWARD': [], 'INPUT': [], 'OUTPUT': []}


# put one statement into filter group

   >>> filter.put_into_fgr("-A  INPUT -s 192.168.1.16/29 -d 172.16.0.0/16 -p tcp -j ACCEPT")
   >>> print filter
   {'FORWARD': [], 'INPUT': ['-A  INPUT -s 192.168.1.16/29 -d 172.16.0.0/16 -p tcp -j ACCEPT'], 'OUTPUT': []}

# add another into OUPTUT chain
   >>> filter.put_into_fgr("-A OUTPUT -d 192.168.1.16/29 -s 172.16.0.0/16 -p tcp -j ACCEPT")
   >>> print filter
   {'FORWARD': [], 'INPUT': ['-A  INPUT -s 192.168.1.16/29 -d 172.16.0.0/16 -p tcp -j ACCEPT'], 'OUTPUT': ['-A OUTPUT -d 192.168.1.16/29 -s 172.16.0.0/16 -p tcp -j ACCEPT']}

# cleanup or factory-reset

   >>> filter.put_into_fgr("-F")
   >>> print filter
   {'FORWARD': [], 'INPUT': [], 'OUTPUT': []}

# filter,  new chain: mychain

   >>> filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
   >>> filter.put_into_fgr("-N mychain")
   >>> print filter
   {'FORWARD': [], 'INPUT': [], 'mychain': [], 'OUTPUT': []}

# one input line for mychain

   >>> filter.put_into_fgr("-A mychain -j DROP")
   >>> print filter
   {'FORWARD': [], 'INPUT': [], 'mychain': ['-A mychain -j DROP'], 'OUTPUT': []}

# remove mychain, factory-reset status

   >>> filter.put_into_fgr("-X mychain")
   >>> print filter
   {'FORWARD': [], 'INPUT': [], 'OUTPUT': []}

# START        rename not yet implemented ####
# make new chain, rename it to firstchain ####

   >>> filter.put_into_fgr("-N mychain")
   >>> filter.put_into_fgr("-E mychain firstchain")
   Unknown filter command in input: -E mychain firstchain
   Not yet implemented, sorry.


   SKIP >>> print filter
   {'FORWARD': [], 'INPUT': [], 'firstchain': [], 'OUTPUT': []}

# END          rename not yet implemented ####

# now remove user-def chain
   SKIP >>> filter.put_into_fgr("-X firstchain")

   SKIP >>> print filter
   {'FORWARD': [], 'INPUT': [], 'OUTPUT': []}

#### Tables object ###########################################################

   >>> tables=Tables("")
   >>> tables.table_printout()
   *raw
   :OUTPUT ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   COMMIT
   *nat
   :OUTPUT ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]
   COMMIT
   *mangle
   :FORWARD ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   :OUTPUT ACCEPT [0:0]
   COMMIT
   *filter
   :FORWARD ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :OUTPUT ACCEPT [0:0]
   COMMIT

# one line input

   >>> tables.put_into_tables('/sbin/iptables -t nat -A PREROUTING -i eth0 -s 192.168.4.113/32 -d 192.168.4.65/32 -p tcp --dport 13080 -j DNAT --to-destination 172.16.0.134:80')
   >>> tables.table_printout()
   *raw
   :OUTPUT ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   COMMIT
   *nat
   :OUTPUT ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]
   -A PREROUTING -i eth0 -s 192.168.4.113/32 -d 192.168.4.65/32 -p tcp --dport 13080 -j DNAT --to-destination 172.16.0.134:80 
   COMMIT
   *mangle
   :FORWARD ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   :OUTPUT ACCEPT [0:0]
   COMMIT
   *filter
   :FORWARD ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :OUTPUT ACCEPT [0:0]
   COMMIT


# second line input

   >>> tables.put_into_tables('/sbin/iptables -A OUTPUT -o eth0 -s 192.168.4.65/32 -d 0.0.0.0/1 -p tcp --sport 1024: --dport 2222 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT -m comment --comment " 0013, 01"')
   >>> tables.table_printout()
   *raw
   :OUTPUT ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   COMMIT
   *nat
   :OUTPUT ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]
   -A PREROUTING -i eth0 -s 192.168.4.113/32 -d 192.168.4.65/32 -p tcp --dport 13080 -j DNAT --to-destination 172.16.0.134:80 
   COMMIT
   *mangle
   :FORWARD ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   :OUTPUT ACCEPT [0:0]
   COMMIT
   *filter
   :FORWARD ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :OUTPUT ACCEPT [0:0]
   -A OUTPUT -o eth0 -s 192.168.4.65/32 -d 0.0.0.0/1 -p tcp --sport 1024: --dport 2222 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT -m comment --comment " 0013, 01" 
   COMMIT


# 3rd line input

   >>> tables.put_into_tables('/sbin/iptables -A INPUT -i eth0 -s 0.0.0.0/1 -d 192.168.4.65/32 -p tcp --sport 2222 --dport 1024: -m state --state ESTABLISHED,RELATED -j ACCEPT -m comment --comment " 0013, 01"')
   >>> tables.table_printout()
   *raw
   :OUTPUT ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   COMMIT
   *nat
   :OUTPUT ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]
   -A PREROUTING -i eth0 -s 192.168.4.113/32 -d 192.168.4.65/32 -p tcp --dport 13080 -j DNAT --to-destination 172.16.0.134:80 
   COMMIT
   *mangle
   :FORWARD ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   :OUTPUT ACCEPT [0:0]
   COMMIT
   *filter
   :FORWARD ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :OUTPUT ACCEPT [0:0]
   -A INPUT -i eth0 -s 0.0.0.0/1 -d 192.168.4.65/32 -p tcp --sport 2222 --dport 1024: -m state --state ESTABLISHED,RELATED -j ACCEPT -m comment --comment " 0013, 01" 
   -A OUTPUT -o eth0 -s 192.168.4.65/32 -d 0.0.0.0/1 -p tcp --sport 1024: --dport 2222 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT -m comment --comment " 0013, 01" 
   COMMIT



# user def chain

   >>> tables.put_into_tables('/sbin/iptables -N tcp__tab')
   >>> tables.put_into_tables('/sbin/iptables -A tcp__tab -s 172.16.100.1/32 -d 192.168.1.149/32 -p tcp --sport 0: --dport ssh -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT -m comment --comment " 0001, 01"')
   >>> tables.table_printout()
   *raw
   :OUTPUT ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   COMMIT
   *nat
   :OUTPUT ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]
   -A PREROUTING -i eth0 -s 192.168.4.113/32 -d 192.168.4.65/32 -p tcp --dport 13080 -j DNAT --to-destination 172.16.0.134:80 
   COMMIT
   *mangle
   :FORWARD ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   :OUTPUT ACCEPT [0:0]
   COMMIT
   *filter
   :FORWARD ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :tcp__tab - [0:0]
   :OUTPUT ACCEPT [0:0]
   -A INPUT -i eth0 -s 0.0.0.0/1 -d 192.168.4.65/32 -p tcp --sport 2222 --dport 1024: -m state --state ESTABLISHED,RELATED -j ACCEPT -m comment --comment " 0013, 01" 
   -A tcp__tab -s 172.16.100.1/32 -d 192.168.1.149/32 -p tcp --sport 0: --dport ssh -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT -m comment --comment " 0001, 01" 
   -A OUTPUT -o eth0 -s 192.168.4.65/32 -d 0.0.0.0/1 -p tcp --sport 1024: --dport 2222 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT -m comment --comment " 0013, 01" 
   COMMIT

# filter flush

   >>> tables.put_into_tables('/sbin/iptables -X tcp__tab')
   >>> tables.put_into_tables('/sbin/iptables -F')
   >>> tables.table_printout()
   *raw
   :OUTPUT ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   COMMIT
   *nat
   :OUTPUT ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]
   -A PREROUTING -i eth0 -s 192.168.4.113/32 -d 192.168.4.65/32 -p tcp --dport 13080 -j DNAT --to-destination 172.16.0.134:80 
   COMMIT
   *mangle
   :FORWARD ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   :OUTPUT ACCEPT [0:0]
   COMMIT
   *filter
   :FORWARD ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :OUTPUT ACCEPT [0:0]
   COMMIT

   >>> tables.put_into_tables('/sbin/iptables -t nat -F')
   >>> tables.table_printout()
   *raw
   :OUTPUT ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   COMMIT
   *nat
   :OUTPUT ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]
   COMMIT
   *mangle
   :FORWARD ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :POSTROUTING ACCEPT [0:0]
   :PREROUTING ACCEPT [0:0]
   :OUTPUT ACCEPT [0:0]
   COMMIT
   *filter
   :FORWARD ACCEPT [0:0]
   :INPUT ACCEPT [0:0]
   :OUTPUT ACCEPT [0:0]
   COMMIT

# ################################################################### #
# EoF
