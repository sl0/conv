#
# -*- coding: utf-8 -*-
#
"""
iptables_converter.py:
    convert iptables commands within a script
    into a correspondig iptables-save script

    default filename to read is rules, to read some other
        file, append: -s filename

    default output is written to stdout, for writing
        to some file, append: -d filename

Author:     Johannes Hubertz <johannes@hubertz.de>
Date:       2017-10-29
version:    0.9.10
License:    GNU General Public License version 3 or later

Have Fun!
"""

from __future__ import print_function

try:
    from collections import UserDict
except ImportError:
    from UserDict import UserDict
from optparse import OptionParser
import re
import sys


class ConverterError(Exception):
    pass


class Chains(UserDict):
    """this is for one type of tables"""

    def __init__(self, name, tables, sloppy=False):
        """init Chains object"""
        UserDict.__init__(self)
        self.name = name
        self.tables = tables
        self.predef = tables
        self.sloppy = sloppy
        self.reset()  # name, tables)

    def put_into_fgr(self, content):
        """fill this line into this tabular"""
        self.length += 1
        cha = "filter"
        # act = ""
        liste = content.split()
        action = liste[0]
        if "-t" in action:
            liste.pop(0)  # remove 1st: -t
            fname = liste.pop(0)
            legals = ["filter", "nat", "raw", "mangle"]
            if fname not in legals:
                msg = "Valid is one of %s, got: %s" % (legals, fname)
                raise ValueError(msg)
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
            if new not in ["ACCEPT", "DROP", "REJECT"]:
                msg = "Illegal policy: % s" % (new)
                raise ValueError(msg)
            self.poli[cha] = new
            return
        if "-X" in action:
            predef = ['INPUT', 'FORWARD', 'OUTPUT',
                      'PREROUTING', 'POSTROUTING']
            rem_chain_name = liste.pop(1)
            if rem_chain_name in predef:
                msg = "Cannot remove predefined chain"
                raise ValueError(msg)
            if rem_chain_name in self.data:
                self.data[rem_chain_name] = []        # empty list
                self.poli[rem_chain_name] = "-"       # empty policy, no need
                self.data.pop(rem_chain_name)
            return
        if "-N" in action:
            new_chain_name = liste.pop(1)
            existing = self.data.keys()
            if new_chain_name in existing:
                msg = "Chain %s already exists" % (new_chain_name)
                raise ValueError(msg)
            self.data[new_chain_name] = []        # empty list
            self.poli[new_chain_name] = "-"       # empty policy, no need
            return
        if "-I" in action:  # or "-A" in action:
            chain_name = liste[1]
            existing = self.data.keys()
            if chain_name not in existing:
                msg = "invalid chain name: %s" % (chain_name)
                if not self.sloppy:
                    raise ValueError(msg)
                else:
                    new_chain_name = liste[1]
                    self.data[new_chain_name] = []
                    self.poli[new_chain_name] = '-'
            kette = self.data[chain_name]
            if len(kette) > 0:
                kette.insert(0, content)
            else:
                msg = "Empty chain %s allows append only!" % (chain_name)
                raise ValueError(msg)
            self.data[chain_name] = kette
            return
        if "-A" in action:  # or "-I" in action:
            chain_name = liste[1]
            existing = self.data.keys()
            if chain_name not in existing:
                msg = "invalid chain name: %s" % (chain_name)
                if not self.sloppy:
                    raise ValueError(msg)
                else:
                    new_chain_name = liste[1]
                    self.data[new_chain_name] = []
                    self.poli[new_chain_name] = '-'
            kette = self.data[chain_name]
            kette.append(content)
            self.data[chain_name] = kette
            return
        msg = "Unknown filter command in input:", content
        raise ValueError(msg)

    def reset(self):  # name, tables):
        """
        name is one of filter, nat, raw, mangle,
        tables is a list of tables in that table-class
        """
        self.poli = {}               # empty dict
        self.length = 0
        self.policy = "-"
        for tabular in self.tables:
            self.data[tabular] = []
            self.poli[tabular] = "ACCEPT"


class Tables(UserDict):
    """
    some chaingroups in tables are predef: filter, nat, mangle, raw
    """

    def __init__(self, fname="reference-one", sloppy=False):
        """init Tables Object is easy going"""
        UserDict.__init__(self)
        self.sloppy = sloppy
        self.reset(fname)

    def reset(self, fname):
        """all predefined Chains aka lists are setup as new here"""
        filters = ["INPUT", "FORWARD", "OUTPUT"]
        filter = Chains("filter", filters, self.sloppy)

        mang = ["PREROUTING", "INPUT", "FORWARD", "OUTPUT", "POSTROUTING", ]
        mangle = Chains("mangle", mang, self.sloppy)

        # kernel 2.6.32 has no INPUT in NAT!
        nats = ["PREROUTING", "OUTPUT", "POSTROUTING"]
        nat = Chains("nat", nats, self.sloppy)

        raws = ["PREROUTING", "OUTPUT", ]
        raw = Chains("raw", raws, self.sloppy)

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
                print("*%s" % (self.data[key].name))
                for chain in self.data[key].keys():
                    poli = self.data[key].poli[chain]
                    print(":%s %s [0:0]" % (chain, poli))
                for chain in self.data[key].values():
                    for elem in chain:
                        print(elem)
                print("COMMIT")

    def put_into_tables(self, line):
        """put line into matching Chains-object"""
        liste = line.split()
        liste.pop(0)                        # we always know, it's iptables
        rest = ""
        for elem in liste:                  # remove redirects and the like
            if ">" not in elem:
                rest = rest + elem + " "    # string again with single blanks
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
                if line.startswith('#'):
                    continue
                for element in ['\$', '\(', '\)', ]:
                    if re.search(element, line):
                        m1 = "Line %d:\n%s\nplain files only, " % \
                             (self.linecounter, line)
                        if element in ['\(', '\)', ]:
                            m2 = "unable to convert shell functions, abort"
                        else:
                            m2 = "unable to resolve shell variables, abort"
                        msg = m1 + m2
                        raise ConverterError(msg)
                for muster in ["^/sbin/iptables ", "^iptables "]:
                    if re.search(muster, line):
                        self.tblctr += 1
                        self.put_into_tables(line)
            fil0.close()
        except (ValueError, IOError) as err:
            raise ConverterError(str(err))
        if not fname == "reference-one":
            print("# generated from: %s" % (fname))


def main():
    """
    main parses options, filnames and the like
    one option (-s) may be given: input-filename
    if none given, it defaults to: rules
    """
    usage = "usage:  %prog --help | -h \n\n\t%prog: version 0.9.10"
    usage = usage + "\tHave Fun!"
    parser = OptionParser(usage)
    parser.disable_interspersed_args()
    parser.add_option("-d", "", dest="destfile",
                      type="string",
                      help="output filename, default: stdout\n")
    parser.add_option("-s", "", dest="sourcefile",
                      type="string",
                      help="file with iptables commands, default: rules\n")
    parser.add_option("--sloppy", "", dest="sloppy",
                      action="store_true", default=False,
                      help="-N name-of-userchain is inserted automatically,\n"
                           "by default -N is neccessary in input\n")
    (options, args) = parser.parse_args()
    if options.sourcefile is None:
        options.sourcefile = "rules"
    sourcefile = options.sourcefile

    try:
        chains = Tables(sourcefile, options.sloppy)
        chains.table_printout()
    except ConverterError as e:
        print(str(e), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
