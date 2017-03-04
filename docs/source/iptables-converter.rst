==========================
iptables-converter - intro
==========================

Default operating
=================

Assume a plain file with following contents::

    iptables -F
    iptables -t nat -F
    iptables -N USER_CHAIN
    iptables -A INPUT -p tcp --dport 23 -j ACCEPT
    iptables -A USER_CHAIN -p icmp -j DROP
    iptables -P INPUT DROP
    iptables -t nat -A POSTROUTING -s 10.0.0.0/21 -p tcp --dport   80 -j SNAT --to-source 192.168.1.15
    iptables -t nat -A PREROUTING  -d 192.0.2.5/32 -p tcp --dport 443 -j DNAT --to-destination 10.0.0.5:1500

As times goes by, the script will grow. The more lines the longer will it take to be loaded.
There should be a quicker way of getting things done. Using iptables-save we easily can save the
actual ruleset from the kernel to a file. To load it's content into the kernel again is a very quick
action compared to the loading of the originating shellscript. So the idea came up to have a
converter just for saving time.

**iptables-converter** by default reads a file **rules**, using comandline parameter ``-s`` any other
file. After having read completely, output is written to stdout for full flexibility.
Given the above file as input the following is printed out::

    *raw
    :OUTPUT ACCEPT [0:0]
    :PREROUTING ACCEPT [0:0]
    COMMIT
    *nat
    :OUTPUT ACCEPT [0:0]
    :PREROUTING ACCEPT [0:0]
    :POSTROUTING ACCEPT [0:0]
    -A PREROUTING -d 192.0.2.5/32 -p tcp --dport 443 -j DNAT --to-destination 10.0.0.5:1500
    -A POSTROUTING -s 10.0.0.0/21 -p tcp --dport 80 -j SNAT --to-source 192.168.1.15
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
    :INPUT DROP [0:0]
    :USER_CHAIN - [0:0]
    :OUTPUT ACCEPT [0:0]
    -A INPUT -p tcp --dport 23 -j ACCEPT
    -A USER_CHAIN -p icmp -j DROP
    COMMIT

As a file this might be read by iptables-restore, which works immediately.

Usage example
-------------

So you probably may want to run the converter from within a shell script
or the like::

    #!/bin/bash

    set -e
    INPUT_FILE=rules
    OUTPUT_FILE=iptables-converted

    # needs to be executable as indicator that writing has ended
    [ ! -r $INPUT_FILE ] && exit 0
    [ ! -x $INPUT_FILE ] && exit 0

    iptables-converter.py -s $INPUT_FILE > $OUTPUT_FILE

    # do it only once!
    mv $INPUT_FILE $INPUT_FILE}.old

    iptables-restore < $OUTPUT_FILE
    echo "$INPUT_FILE successfully converted and loaded"
    exit 0
    # EoF



Error handling
==============

Shell functions and shell commands
----------------------------------

As the file read is not interpreted in any way, there are few known error conditions:

  #) the file contains some shell variables, indicated by '$',
     this leads to an errormessage and exits immediately with returncode 1.
  #) the file contains some shell functions, indicated by '(' and/or ')',
     this leads to an errormessage and exits immediately with returncode 1.

If you have such a file, and you want to speed up by converting, please
execute it and feed the output as a file to iptables-converter.


Non exsitent user chains
------------------------

iptables-converter does some more error-checking while reading input.

Normal behavior is to raise an errror, if any append or insert
statement to an userdefined chain is not preceeded by a corresonding
creation statement '-N'. This may be changed to a more smooth
handling with an additional commandline option '- - sloppy'.
Having this, a non existent userchain is created on the fly when
the first append statement is seen. So it is set as first entry gracefully.

Inserting into an emtpy chain anyhow raises an error as iptables-restore
would do it later on trying to set the files content into the kernel.

Just to mention it: **iptables -E xyz** and **iptables -L** are not implemented and throw exceptions for now!
