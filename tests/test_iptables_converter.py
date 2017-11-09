#!/usr/bin/env python

#encoding:utf8

from iptables_conv.iptables_converter import Chains, Tables, ConverterError
import unittest
import sys

dst = sys.stdout


class Chains_Test(unittest.TestCase):
    '''some tests for class Chain'''

    def test_01_create_a_chain_object(self):
        """
        Chain 01: create a Filter group, f.e. filter
        """
        self.assertIsInstance(Chains("filter",
                                     ["INPUT", "FORWARD", "OUTPUT"]), Chains)
        self.assertEquals({}, Chains("filter", []))
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        self.assertEquals("filter", filter.name)
        self.assertEquals(['INPUT', 'FORWARD', 'OUTPUT'], filter.tables)
        self.assertEquals("-", filter.policy)
        self.assertEquals(0, filter.length)
        self.assertEquals(
            {'FORWARD': 'ACCEPT', 'INPUT': 'ACCEPT', 'OUTPUT': 'ACCEPT'},
            filter.poli)

    def test_02_prove_policies(self):
        """
        Chain 02: check 3 valid policies, 1 exception
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        filter.put_into_fgr("-P INPUT DROP")
        self.assertEquals(
            {'FORWARD': 'ACCEPT', 'INPUT': 'DROP', 'OUTPUT': 'ACCEPT'},
            filter.poli)
        filter.put_into_fgr("-P FORWARD REJECT")
        self.assertEquals(
            {'FORWARD': 'REJECT', 'INPUT': 'DROP', 'OUTPUT': 'ACCEPT'},
            filter.poli)
        filter.put_into_fgr("-P OUTPUT DROP")
        self.assertEquals(
            {'FORWARD': 'REJECT', 'INPUT': 'DROP', 'OUTPUT': 'DROP'},
            filter.poli)
        with self.assertRaises(ConverterError):
            filter.put_into_fgr("-P OUTPUT FAIL")

    def test_03_tables_names(self):
        """
        Chain 03: 3 cases OK, 1 Exception
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        filter.put_into_fgr("-t filter -A INPUT -i sl0 -j ACCEPT")
        self.assertEquals(['-A INPUT -i sl0 -j ACCEPT '], filter.data["INPUT"])

        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        filter.put_into_fgr("-t nat -A OUTPUT -j ACCEPT")
        self.assertEquals(['-A OUTPUT -j ACCEPT '], filter.data["OUTPUT"])

        filter.put_into_fgr("-t nat -A FORWARD -j ACCEPT")
        self.assertEquals(['-A FORWARD -j ACCEPT '], filter.data["FORWARD"])

        with self.assertRaises(ConverterError):
            filter.put_into_fgr("-t na -A INPUT")

    def test_04_flush(self):
        """
        Chain 04: flush filter group, 2 rules and an invalid chain
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        filter.put_into_fgr("-t filter -A INPUT -i sl0 -j ACCEPT")
        self.assertEquals(['-A INPUT -i sl0 -j ACCEPT '],
                          filter.data["INPUT"])
        filter.put_into_fgr("-A OUTPUT -o sl1 -j ACCEPT")
        self.assertEquals(['-A OUTPUT -o sl1 -j ACCEPT'],
                          filter.data["OUTPUT"])

        filter.put_into_fgr("-F")
        self.assertEquals([], filter.data["INPUT"])
        self.assertEquals([], filter.data["OUTPUT"])

        with self.assertRaises(ConverterError):
            filter.put_into_fgr("-t inval -F")

    def test_05_new_chain(self):
        """
        Chain 05: create a new chain in filtergroup,
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        filter.put_into_fgr("-N NEWCHAIN")
        self.assertEquals(
            {'FORWARD': [], 'INPUT': [], 'NEWCHAIN': [], 'OUTPUT': []},
            filter.data)

    def test_06_new_existing_chain_fails(self):
        """
        Chain 06: create an exsiting chain should fail
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        with self.assertRaises(ConverterError):
            filter.put_into_fgr("-N INPUT")

    def test_07_insert_rule_fail(self):
        """
        Chain 07: insert a rule into an empty chain fails
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        with self.assertRaises(ConverterError):
            filter.put_into_fgr("-I INPUT -j ACCEPT")

    def test_08_insert_rule_fail(self):
        """
        Chain 08: insert a rule into a non_existing chain fails
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        with self.assertRaises(ConverterError):
            filter.put_into_fgr("-I PUT -j ACCEPT")

    def test_09_insert_rule_works(self):
        """
        Chain 09: insert a rule into a nonempty chain works at start
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        filter.put_into_fgr("-A INPUT -p tcp -j ACCEPT")
        filter.put_into_fgr("-I INPUT -p udp -j ACCEPT")
        filter.put_into_fgr("-I INPUT -p esp -j ACCEPT")
        expect = ['-I INPUT -p esp -j ACCEPT',
                  '-I INPUT -p udp -j ACCEPT',
                  '-A INPUT -p tcp -j ACCEPT']
        self.assertEquals(expect, filter.data["INPUT"])

    def test_10_append_rule(self):
        """
        Chain 10: append a rule to a chain
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        filter.put_into_fgr("-A INPUT -p tcp -j ACCEPT")
        self.assertEquals(['-A INPUT -p tcp -j ACCEPT'], filter.data["INPUT"])
        filter.put_into_fgr("-A INPUT -p udp -j ACCEPT")
        filter.put_into_fgr("-A INPUT -p esp -j ACCEPT")
        expect = ['-A INPUT -p tcp -j ACCEPT',
                  '-A INPUT -p udp -j ACCEPT',
                  '-A INPUT -p esp -j ACCEPT']
        self.assertEquals(expect, filter.data["INPUT"])

    def test_11_remove_predef_chain(self):
        """
        Chain 11: try to remove a prefined chain
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        with self.assertRaises(ConverterError):
            filter.put_into_fgr("-X INPUT")

    def test_12_remove_chain(self):
        """
        Chain 12: try to remove an existing chain
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        filter.put_into_fgr("-N NEWCHAIN")
        self.assertEquals(
            {'FORWARD': [], 'INPUT': [], 'NEWCHAIN': [], 'OUTPUT': []},
            filter.data)
        filter.put_into_fgr("-X NEWCHAIN")
        self.assertEquals(
            {'FORWARD': [], 'INPUT': [], 'OUTPUT': []},
            filter.data)

    def test_13_illegal_command(self):
        """
        Chain 13: try an ilegal command
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        with self.assertRaises(ConverterError):
            filter.put_into_fgr("-Y USERCHAIN")


class Tables_Test(unittest.TestCase):
    '''
    Tables: some first tests for the class
    '''

    def test_01_create_a_tables_object(self):
        """
        Tables 01: create a Tables object, check chains
        """
        self.assertIsInstance(Tables(dst, ""), Tables)

        tables = Tables(dst, "")
        expect = {'filter': {'FORWARD': [], 'INPUT': [], 'OUTPUT': []},
                  'raw': {'OUTPUT': [], 'PREROUTING': []},
                  'mangle': {'FORWARD': [], 'INPUT': [],
                             'POSTROUTING': [], 'PREROUTING': [], 'OUTPUT': []},
                  'nat': {'OUTPUT': [], 'PREROUTING': [], 'POSTROUTING': []}}
        self.assertEquals(expect, tables.data)

    def test_02_nat_prerouting(self):
        """
        Tables 02: nat PREROUTING entry
        """
        tables = Tables(dst, "")
        line = "iptables -t nat -A PREROUTING -s 10.0.0.0/21"
        line = line + " -p tcp --dport   80 -j SNAT --to-source 192.168.1.15"
        tables.put_into_tables(line)
        expect = ['-A PREROUTING -s 10.0.0.0/21 -p tcp --dport 80 -j SNAT --to-source 192.168.1.15 ']
        self.assertEquals(expect, tables.data["nat"]["PREROUTING"])

    def test_03_mangle_table(self):
        """
        Tables 03: mangle INPUT entry
        """
        tables = Tables(dst, "")
        line = "iptables -t mangle -A INPUT"
        line = line + " -p tcp --dport   80 -j ACCEPT"
        tables.put_into_tables(line)
        expect = ['-A INPUT -p tcp --dport 80 -j ACCEPT ']
        self.assertEquals(expect, tables.data["mangle"]["INPUT"])

    def test_04_raw_table(self):
        """
        Tables 04: raw OUTPUT entry
        """
        tables = Tables(dst, "")
        line = "iptables -t raw -A OUTPUT"
        line = line + " -p tcp --dport   80 -j ACCEPT"
        tables.put_into_tables(line)
        expect = ['-A OUTPUT -p tcp --dport 80 -j ACCEPT ']
        self.assertEquals(expect, tables.data["raw"]["OUTPUT"])

    def test_05_not_existing_chain(self):
        """
        Tables 05: INPUT to not existing chain
        """
        line = "iptables -t raw -A NONEXIST -p tcp --dport   80 -j ACCEPT"
        with self.assertRaises(ConverterError):
            Tables(dst, "").put_into_tables(line)

    def test_06_read_not_existing_file(self):
        """
        Tables 06: read non existing file
        """
        with self.assertRaises(ConverterError):
            Tables(dst, "not-exist-is-ok")

    def test_07_read_empty_file(self):
        """
        Tables 07: read empty file (in relation to iptables-commands)
        """
        filename = "MANIFEST.in"
        tables = Tables(dst, filename)
        expect = {'filter': {'FORWARD': [], 'INPUT': [], 'OUTPUT': []},
                  'raw': {'OUTPUT': [], 'PREROUTING': []},
                  'mangle': {'FORWARD': [], 'INPUT': [], 'POSTROUTING': [],
                             'PREROUTING': [], 'OUTPUT': []},
                  'nat': {'OUTPUT': [], 'PREROUTING': [], 'POSTROUTING': []}}
        self.assertEquals(expect, tables.data)

    def test_08_reference_one(self):
        """
        Tables 08: read default file: reference-one, check chains
        """
        tables = Tables(dst)
        expect = {
            'filter': {'FORWARD': [],
                       'INPUT': ['-A INPUT -p tcp --dport 23 -j ACCEPT '],
                       'USER_CHAIN': ['-A USER_CHAIN -p icmp -j DROP '],
                       'OUTPUT': []},
            'raw': {'OUTPUT': [], 'PREROUTING': []},
            'mangle': {'FORWARD': [], 'INPUT': [], 'POSTROUTING': [],
                       'PREROUTING': [], 'OUTPUT': []},
            'nat': {'OUTPUT': [],
                    'POSTROUTING': ['-A POSTROUTING -s 10.0.0.0/21 -p tcp --dport 80 -j SNAT --to-source 192.168.1.15 '],
                    'PREROUTING': ['-A PREROUTING -d 192.0.2.5/32 -p tcp --dport 443 -j DNAT --to-destination 10.0.0.5:1500 ']}}
        self.maxDiff = None
        self.assertEquals(expect, tables.data)

    def test_09_shell_variables(self):
        """
        Tables 09: read buggy file with shell variables
        """
        expect = "Line 8:"
        with self.assertRaisesRegexp(ConverterError, expect):
            Tables(dst, 'tests/data/test-shell-variables')

    def test_10_shell_functions(self):
        """
        Tables 10: read buggy file with shell functions
        """
        expect = "Line 6:"
        with self.assertRaisesRegexp(ConverterError, expect):
            Tables(dst, 'tests/data/test-debian-bug-no-748638')

    def test_11_reference_sloppy_one(self):
        """
        Tables 11: read sloppy input file: reference-sloppy-one, check chains
        """
        tables = Tables(dst, 'reference-sloppy-one', True)
        expect = {
            'filter':
                {'FORWARD': [], 'INPUT': ['-A INPUT -p tcp --dport 23 -j ACCEPT '],
                 'USER_CHAIN': ['-I USER_CHAIN -p icmp --icmp-type echo-request -j ACCEPT ',
                                '-A USER_CHAIN -p icmp --icmp-type echo-reply -j ACCEPT ',
                                '-A USER_CHAIN -p icmp -j DROP '], 'OUTPUT': []},
            'raw': {'OUTPUT': [], 'PREROUTING': []},
            'mangle': {'FORWARD': [], 'INPUT': [], 'POSTROUTING': [], 'PREROUTING': [], 'OUTPUT': []},
            'nat': {'OUTPUT': [],
                    'PREROUTING': ['-A PREROUTING -d 192.0.2.5/32 -p tcp --dport 443 -j DNAT --to-destination 10.0.0.5:1500 '],
                    'POSTROUTING': ['-A POSTROUTING -s 10.0.0.0/21 -p tcp --dport 80 -j SNAT --to-source 192.168.1.15 ']}
        }
        self.maxDiff = None
        self.assertEqual(expect, tables.data)

    def test_12_create_a_tables6_object(self):
        """
        Tables 12: create an ipv6 Tables object, check chains
        """
        self.assertIsInstance(Tables(dst, "", ipversion=6), Tables)

        tables = Tables(dst, "", ipversion=6)
        expect = {'filter': {'FORWARD': [], 'INPUT': [], 'OUTPUT': []},
                  'raw': {'OUTPUT': [], 'PREROUTING': []},
                  'mangle': {'FORWARD': [], 'INPUT': [],
                             'POSTROUTING': [], 'PREROUTING': [], 'OUTPUT': []},
                  'nat': {'OUTPUT': [], 'PREROUTING': [], 'POSTROUTING': []}}
        self.assertEquals(expect, tables.data)

    def test_13_re6ference_one(self):
        """
        Tables 13: read default file: re6ference-one, check chains
        """
        tables = Tables(dst, "re6ference-one", ipversion=6)
        expect = {
            'filter': {'FORWARD': [],
                       'INPUT': ['-A INPUT -p tcp --dport 23 -j ACCEPT '],
                       'USER_CHAIN': ['-A USER_CHAIN -p icmp -j DROP '], 'OUTPUT': []},
            'raw': {'OUTPUT': [], 'PREROUTING': []},
            'mangle': {'FORWARD': [], 'INPUT': [], 'POSTROUTING': [], 'PREROUTING': [], 'OUTPUT': []},
            'nat': {'OUTPUT': [], 'PREROUTING': ['-A PREROUTING -d 2001:db8:feed::1/128 -p tcp --dport 443 -j DNAT --to-destination 2001:db8:feed::1:1500 '], 'POSTROUTING': ['-A POSTROUTING -s 2001:db8:dead::/64 -p tcp --dport 80 -j SNAT --to-source 2001:db8:feed::1 ']}
        }
        self.maxDiff = None
        self.assertEquals(expect, tables.data)

    def test_14_re6ference_sloppy_one(self):
        """
        Tables 14: read sloppy input file: re6ference-sloppy-one, check chains
        """
        tables = Tables(dst, 're6ference-sloppy-one', sloppy=True, ipversion=6)
        expect = {
            'filter':
                {'FORWARD': [], 'INPUT': ['-A INPUT -p tcp --dport 23 -j ACCEPT '],
                 'USER_CHAIN': ['-A USER_CHAIN -p icmp -j DROP '], 'OUTPUT': []},
            'raw': {'OUTPUT': [], 'PREROUTING': []},
            'mangle': {'FORWARD': [], 'INPUT': [], 'POSTROUTING': [], 'PREROUTING': [], 'OUTPUT': []},
            'nat': {'OUTPUT': [],
                    'PREROUTING':
                    ['-A PREROUTING -d 2001:db8:feed::1/128 -p tcp --dport 443 -j DNAT --to-destination 2001:db8:feed::1:1500 '],
                    'POSTROUTING':
                    ['-A POSTROUTING -s 2001:db8:dead::/64 -p tcp --dport 80 -j SNAT --to-source 2001:db8:feed::1 ']}
        }
        self.maxDiff = None
        self.assertEqual(expect, tables.data)


def test_15_tables_printout(capsys):
    """
    Tables 15: check table_printout as well
    """
    tables = Tables(sys.stdout, 'reference-one')
    tables.table_printout()
    out, err = capsys.readouterr()
    assert len(err) == 0
    words = ['*raw', '*nat', '*mangle', '*filter', 'COMMIT', 'from:',
             'INPUT', 'FORWARD', 'USER_CHAIN', '192.0.2.5', ]
    absents = ['iptables', '-t raw', '-t mangle', 'udp', ]
    for word in words:
        assert word in out
    for absent in absents:
        assert absent not in out


if __name__ == "__main__":
        unittest.main()
