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
Date:       2017-11-04
Version:    see __init__.version
License:    GNU General Public License version 3 or later
            Apache License Version 2.0

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
from .__init__ import __version__


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
        if len(content) == 0:
            return
        # act = ""
        liste = content.split()
        action = liste[0]
        if "-t" in action:
            liste.pop(0)  # remove 1st: -t
            fname = liste.pop(0)
            legals = ["filter", "nat", "raw", "mangle"]
            if fname not in legals:
                msg = "Valid is one of %s, got: %s" % (legals, fname)
                raise ConverterError(msg)
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
                raise ConverterError(msg)
            self.poli[cha] = new
            return
        if "-X" in action:
            predef = ['INPUT', 'FORWARD', 'OUTPUT',
                      'PREROUTING', 'POSTROUTING']
            rem_chain_name = liste.pop(1)
            if rem_chain_name in predef:
                msg = "Cannot remove predefined chain"
                raise ConverterError(msg)
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
                raise ConverterError(msg)
            self.data[new_chain_name] = []        # empty list
            self.poli[new_chain_name] = "-"       # empty policy, no need
            return
        if "-I" in action:  # or "-A" in action:
            chain_name = liste[1]
            existing = self.data.keys()
            if chain_name not in existing:
                msg = "invalid chain name: %s" % (chain_name)
                if not self.sloppy:
                    raise ConverterError(msg)
                else:
                    new_chain_name = liste[1]
                    self.data[new_chain_name] = []
                    self.poli[new_chain_name] = '-'
            kette = self.data[chain_name]
            if len(kette) > 0:
                kette.insert(0, content)
            else:
                msg = "Empty chain %s allows append only!" % (chain_name)
                raise ConverterError(msg)
            self.data[chain_name] = kette
            return
        if "-A" in action:  # or "-I" in action:
            chain_name = liste[1]
            existing = self.data.keys()
            if chain_name not in existing:
                msg = "invalid chain name: %s" % (chain_name)
                if not self.sloppy:
                    raise ConverterError(msg)
                else:
                    new_chain_name = liste[1]
                    self.data[new_chain_name] = []
                    self.poli[new_chain_name] = '-'
            kette = self.data[chain_name]
            kette.append(content)
            self.data[chain_name] = kette
            return
        msg = "Unknown filter command in input:" + content
        raise ConverterError(msg)

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

    def __init__(self,
                 destfile,
                 sourcefile="reference-one",
                 sloppy=False,
                 ipversion=4
                 ):
        """init Tables Object is easy going"""
        UserDict.__init__(self)
        self.destfile = destfile
        self.sourcefile = sourcefile
        self.sloppy = sloppy
        self.patterns = ""
        self.reset(sourcefile, ipversion)

    def reset(self, sourcefile, ipversion):
        """all predefined Chains aka lists are setup as new here"""
        self.patterns = ['^iptables', '^/sbin/iptables', ]
        if ipversion == 6:
            self.patterns = ['^ip6tables', '^/sbin/ip6tables', ]

        filt = ["INPUT", "FORWARD", "OUTPUT"]
        filters = Chains("filter", filt, self.sloppy)

        mang = ["PREROUTING", "INPUT", "FORWARD", "OUTPUT", "POSTROUTING", ]
        mangle = Chains("mangle", mang, self.sloppy)

        # kernel 2.6.32 has no INPUT in NAT!
        nats = ["PREROUTING", "OUTPUT", "POSTROUTING"]
        nat = Chains("nat", nats, self.sloppy)

        raws = ["PREROUTING", "OUTPUT", ]
        raw = Chains("raw", raws, self.sloppy)

        self.data["filter"] = filters
        self.data["mangle"] = mangle
        self.data["nat"] = nat
        self.data["raw"] = raw
        if len(sourcefile) > 0:
            self.linecounter = self.read_file(sourcefile)

    def table_printout(self):
        """printout nonempty tabulars in fixed sequence"""
        self.destfile.write("# generated from: %s\n" % (self.sourcefile))
        for key in ["raw", "nat", "mangle", "filter"]:
            count = self.data[key].length
            if count > -1:
                self.destfile.write("*%s\n" % (self.data[key].name))
                for chain in self.data[key].keys():
                    poli = self.data[key].poli[chain]
                    self.destfile.write(":%s %s [0:0]\n" % (chain, poli))
                for chain in self.data[key].values():
                    for elem in chain:
                        self.destfile.write(elem)
                        self.destfile.write('\n')
                self.destfile.write("COMMIT\n")

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

    def read_file(self, sourcefile):
        try:
            with open(sourcefile, 'r') as f:
                return self.read(f)
        except IOError as err:
            raise ConverterError(str(err))

    def read(self, fd):
        """read data from file like object into Tables-object"""
        self.linecounter = 0
        self.tblctr = 0
        try:
            for zeile in fd:
                line = str(zeile.strip())
                self.linecounter += 1
                if line.startswith('#'):
                    continue
                for element in ['\$', '\(', '\)', ]:
                    if re.search(element, line):
                        mstart = "Line %d:\n%s\nplain files only, " % \
                            (self.linecounter, line)
                        if element in ['\(', '\)', ]:
                            merr = "unable to convert shell functions, abort"
                        else:
                            merr = "unable to resolve shell variables, abort"
                        msg = mstart + merr
                        raise ConverterError(msg)
                for pattern in self.patterns:
                    if re.search(pattern, line):
                        self.tblctr += 1
                        self.put_into_tables(line)
        except ValueError as err:
            raise ConverterError(str(err))


def main():
    """
    main parses options, filnames and the like
    option -s needs input-filename to be read,
    if it is not given, it defaults to: rules.
    option -d needs output-filename to be written,
    if it is not given, it defaults to: sys.stdout
    """
    version = "version %s" % __version__
    usage = "usage:  %prog --help | -h \n\n\t%prog: " + version
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
    (options, _) = parser.parse_args()

    if options.sourcefile is None:
        options.sourcefile = "rules"
    sourcefile = options.sourcefile

    if options.destfile is not None:
        destfile = open(options.destfile, 'w')
    else:
        destfile = sys.stdout

    ipversion = 4
    if '6' in sys.argv[0]:
        ipversion = 6

    try:
        chains = Tables(destfile,
                        sourcefile,
                        options.sloppy,
                        ipversion=ipversion
                        )
        chains.table_printout()
    except ConverterError as err:
        print(str(err), file=sys.stderr)
        return 1
    finally:
        if destfile != sys.stdout:
            destfile.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
