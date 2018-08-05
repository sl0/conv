================================
iptables-converter - description
================================

In linux iptables exists since kernel version 2.4.

A corresponding userland command **iptables** is used to
control them.

The tables are grouped in filter, nat, mangle and raw.
In every group there are chains, which contain more or
less traffic specific rules. Predefined in filter tables
are INPUT, FORWARD and OUTPUT chain. Perhaps you like to
read the fine manuals about the iptables command in Linux
to get to know more about these.

Usually a systemadministrator wants to write his rules in
a shell script, which is run within the boot sequence or
every now and then on every change... Over the time this
script will grow. The longer it gets, the more time takes
it to complete. Exactly this is the reason, why
**iptables-converter** was written. Only motivation was to
speed up the loading of long scripts with multiple iptables
commands.

The **iptables-converter** is a pure python script with
two entrypoints:

- **iptables-converter**
- **ip6tables-converter**

They reside in linux userland, that means to run one of them
you don't need root priviledges, which are only needed to load
the output of the converters into the kernelspace.

Command line interface
======================

To have an idea which command line options are supported,
just ask it for help::

    $ iptables-converter --help
    Usage:  iptables-converter --help | -h

            iptables-converter: version 0.9.11  Have Fun!

    Options:
      -h, --help            show this help message and exit
      -d DESTFILE, --dest-file=DESTFILE
                            output filename, default: stdout
      -s SOURCEFILE, --source-file=SOURCEFILE
                            file with iptables commands, default: rules
      --sloppy              -N name-of-userchain is inserted automatically, by
                            default -N is neccessary in input

**ip6tables-converter** surprisingly behaves exactly the same way, except from
the '6' in the command and version line::

    $ ip6tables-converter --help
    Usage:  ip6tables-converter --help | -h

        ip6tables-converter: version 0.9.11 Have Fun!

    Options:
      -h, --help            show this help message and exit
      -d DESTFILE, --dest-file=DESTFILE
                            output filename, default: stdout
      -s SOURCEFILE, --source-file=SOURCEFILE
                            file with iptables commands, default: rules
      --sloppy              -N name-of-userchain is inserted automatically, by
                            default -N is neccessary in input

The only difference in between them is what is looked at.
iptables-converter just handles lines starting with
**iptables** or **/sbin/iptables**, ip6tables-converter
only lines starting with **ip6tables** or **/sbin/ip6tables**.

DEST- and SOURCEFILE
--------------------

These should be clear, the default values are build in for
your convenience only. A script generating iptables command
writes them into a file named *rules*, which is then read by
the converter, if the **-s** option is not used. The converters
ouptut is then written to **stdout**, if the **-d** option is
not used. So it might be piped or somehow else processed.

--sloppy
--------

The option **--sloppy** perhaps needs some explanation.
Usually the iptables command insists on defined chains,
especially you cannot insert or append a rule into a
non-existent user defined chain. Especially the
**-N UserChain** is needed normally in advance to the
append operation. Inserting into an empty chain is
forbidden as well. By using the **--sloppy** option this
**-N** command is not needed in the input for the
converter as it defines the UserCHain automatically on
the first occurance of any.


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

As times goes by, this script will grow. The more lines
it has, the longer will it take to be loaded. This is
because every iptables statement needs to modify the
kernels iptables as an atomar operation, which is a
lot of overhead from locking the tables, modifying
and unlocking them. There should be a quicker way of
getting things done. Using iptables-save we can save
easily the actual ruleset from the kernel to a file.
To load it's content into the kernel again is a very
quick action compared to the loading of the originating
shellscript. The iptables-restore operation is one
atomar operation from the kernels view regardless of
the number of modifications. It's clear to be the much
quicker the more lines are covered. The disadvantage
of this proceeding is, the table, f.e. the filter
tables, are loaded at once, i.e. no appending or
inserterting using the *same* command is possible.
You only need a complete set of iptable commands
within a file, just like iptables-save gives it.
So the idea came up to have a converter just for
saving time.

Lets assume, the file shown above is named **generated-rules**,
then we have easy going::

    $ iptables-converter -s generated-rules -d converted-rules
    $ cat converted-rules
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
    $

On the same machine or after beeing transferred to another
one, the **converted-rules** file can be loaded into the kernel
by using the command **iptables-restore** as *root user*::

    # iptables-restore -c converted-rules

Of course you use pathnames where filenames are mentioned.

Usage example
-------------

So you probably may want to run the converter
from within a shell script or the like::

    #!/bin/bash

    set -e
    INPUT_FILE=rules
    OUTPUT_FILE=iptables-converted

    # needs to be executable as indicator that writing has ended
    [ ! -r $INPUT_FILE ] && exit 0
    [ ! -x $INPUT_FILE ] && exit 0

    iptables-converter.py -s $INPUT_FILE -d $OUTPUT_FILE

    # do it only once!
    mv $INPUT_FILE $INPUT_FILE}.old

    iptables-restore < $OUTPUT_FILE
    echo "$INPUT_FILE successfully converted and loaded"
    exit 0
    # EoF



Error handling
==============

In accidental cases of errors the converter should give you a
traceback wherin the word **ConverterError** appears. This is to
let you get to know, where in your whole programming universe
the error happend.

Two things can not be handled: Shell functions and shell
variables, because the converter does not interpret your
input-file.

Shell functions and shell commands
----------------------------------

As the file which is read is not interpreted
in any way, there are few known error conditions:

  #) the file contains some shell variables, indicated by '$',
     this leads to an errormessage and exits immediately with returncode 1.
  #) the file contains some shell functions, indicated by '(' and/or ')',
     this leads to an errormessage and exits immediately with returncode 1.

If you have such a file, and you want to speed up by converting, please
execute it and feed the output as a file to iptables-converter.


Non existent user chains
------------------------

iptables-converter does some more error-checking while reading input.

Normal behavior is to raise an **ConverterError**, if any append or insert
statement to an userdefined chain is not preceeded by a corresonding chain
creation statement '-N'. This may be changed to a more smooth
handling with an additional commandline option **--sloppy**.
Having this, a non existent userchain is created on the fly when
the first append statement is seen. So it is set as first entry gracefully.

Inserting into an emtpy chain anyhow raises an error as iptables-restore
would do it later on trying to set the files content into the kernel.

Not implemented
---------------

Just to mention it: **iptables -E xyz** and **iptables -L** are not
implemented in the **iptables-converter** and throw exceptions for now!
