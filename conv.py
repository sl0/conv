#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
"""
conv.py: convert iptables commands within a script
into a correspondig iptables-save script

default filename to read is rules, to read some other
        file, append: -s filename

output is written to stdout for maximum flexibilty

Author:     sl0.self@googlemail.com
Date:       2012-12-15
Version:    0.2
License:    GNU General Public License version 3 or later

Have Fun!
"""

from UserDict import UserDict
from optparse import OptionParser
import re
import sys


class Chains(UserDict):
    """this is for one type of tables"""

    def __init__(self, name, tables):
        """init Chains object"""
        UserDict.__init__(self)
        self.name = name
        self.tables = tables
        self.predef = tables
        self.reset() #name, tables)

    def put_into_fgr(self, content):
        """fill this line into this tabular"""
        #print "put_into_fgr:", self.name, action, content
        self.length += 1
        cha = "filter"
        #act = ""
        liste = content.split()
        action = liste[0]
        if "-t" in action:
            liste.pop(0) # remove 1st: -t
            liste.pop(0) # remove 1st: nat
            action = liste[0]
            content = ""                       # rebuild content from here
            for elem in liste:
                content = content + elem + " "
            if len(liste) > 1:
                chain_name = liste[1]
        if "-F" in action:
            self.reset()
            return
        if "-P" in action:
            liste.pop(0)
            cha = liste.pop(0)
            new = liste.pop(0)
            self.poli[cha] = new
            return
        if "-X" in action:
            rem_chain_name = liste.pop(1)
            if rem_chain_name in self.data:
                self.data[rem_chain_name] = []        # empty list
                self.poli[rem_chain_name] = "-"       # empty policy, no need
                self.data.pop(rem_chain_name)
            return
        if "-N" in action:
            new_chain_name = liste.pop(1)
            self.data[new_chain_name] = []        # empty list
            self.poli[new_chain_name] = "-"       # empty policy, no need
            return
        if "-I" in action: # or "-A" in action:
            chain_name = liste[1]
            kette = self.data[chain_name]
            kette.insert(0, content)
            self.data[chain_name] = kette
            return
        if "-A" in action: # or "-I" in action:
            chain_name = liste[1]
            kette = self.data[chain_name]
            kette.append(content)
            self.data[chain_name] = kette
            return
        print "Unknown filter command in input:", content
        print "Not yet implemented, sorry."
        return

    def reset(self): # name, tables):
        """
        name is one of filter, nat, raw, mangle,
        tables is a list of tables in that table-class
        """
        self.poli = {}               # empty dict
        self.length = 0
        self.policy = "-"
        for tabular in self.tables:
            self.data[tabular] = []    #print "# init:", name, tabular
            self.poli[tabular] = "ACCEPT"


class Tables(UserDict):
    """
    some tables are predef: filter, nat, mangle, raw"""

    def __init__(self, fname):
        """init Tables Object is easy going"""
        UserDict.__init__(self)
        self.reset(fname)

    def reset(self, fname):
        """all predefined Chains aka lists are setup as new here"""
        #print "# reading:", fname
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])

        mang = ["PREROUTING", "INPUT", "FORWARD", "OUTPUT", "POSTROUTING", ]
        mangle = Chains("mangle", mang)

        # kernel 2.6.32 has no INPUT in NAT!
        nat = Chains("nat", ["PREROUTING", "OUTPUT", "POSTROUTING"])

        raw = Chains("raw", ["PREROUTING", "OUTPUT", ])

        self.data["filter"] = filter
        self.data["mangle"] = mangle
        self.data["nat"] = nat
        self.data["raw"] = raw
        if len(fname) > 0:
            self.linecounter = self.read_file(fname)

    def table_printout(self):
        """printout nonempty tabulars in fixed sequence"""
        for key in ["raw", "nat", "mangle", "filter"]:
            len = self.data[key].length
            if len > -1:
                print "*%s" % (self.data[key].name)
                for chain in self.data[key].keys():
                    #print type(self.data[key]), type(chain)
                    poli = self.data[key].poli[chain]
                    print ":%s %s [0:0]" % (chain, poli)
                for chain in self.data[key].values():
                    for elem in chain:
                        print elem
                print "COMMIT"

    def put_into_tables(self, line):
        """put line into matching Chains-object"""
        liste = line.split()
        liste.pop(0)                        # we always know, it's iptables
        rest = ""
        for elem in liste:                  # remove redirects and the like
            if ">" not in elem:
                rest = rest + elem + " "    # string again with single blanks
        action = liste.pop(0)               # action is one of {N,F,A,I, etc.}
        fam = "filter"
        if "-t nat" in line:                # nat filter group
            fam = "nat"
        elif "-t mangle" in line:           # mangle filter group
            fam = "mangle"
        elif "-t raw" in line:              # raw filter group
            fam = "raw"
        fam_dict = self.data[fam]           # select the group dictionary
        fam_dict.put_into_fgr(rest)         # do action thers

    def read_file(self, fname):
        """read file into Tables-object"""
        self.linecounter = 0
        self.tblctr = 0
        try:
            fil0 = open(fname, 'r')
            for zeile in fil0:
                line = str(zeile.strip())
                self.linecounter += 1
                for muster in ["^/sbin/iptables ", "^iptables "]:
                    if re.search(muster, line) > 0:
                        self.tblctr += 1
                        self.put_into_tables(line)
            fil0.close()
        except IOError, err:
            print fname + ": ", err.strerror
            sys.exit(1)
        print "# generated from: %s" % (fname)


def main():
    """
    main parses options, filnames and the like
    one option (-s) may be given: input-filename
    if none given, it defaults to: rules
    """
    usage = "usage:  %prog --help | -h \n\n\t%prog: version 0.1"
    usage = usage + "\tHave Fun!"
    parser = OptionParser(usage)
    parser.disable_interspersed_args()
    parser.add_option("-s", "", #"--source-file",
                        dest = "sourcefile",
                        help = "file with iptables commands, default: rules\n")
    #parser.add_option("-d", "", #"--destiantion-file",
    #                    dest = "destination",
    #                    help = "file iptables-save are written to, \
    #                           default: rules-saved")
    (options, args) = parser.parse_args()
    hlp = "\n\tplease use \"--help\" as argument, abort!\n"
    if options.sourcefile == None:
        options.sourcefile = "rules"
    sourcefile = options.sourcefile
    #if options.destination == None:
    #    options.destination = sourcefile + "-saved-conv"
    #destination = options.destination

    chains = Tables(sourcefile)
    chains.table_printout()

    sys.exit(0)

if __name__ == "__main__":
    main()
