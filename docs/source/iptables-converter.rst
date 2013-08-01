==========================
iptables-converter - intro
==========================

Assume a shell-script containing the following content::

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

iptables-converter does some error-checking while reading input. 
Just to mention it: **iptables -E xyz** and **iptables -L** are not implemented and throw exceptions for now!
