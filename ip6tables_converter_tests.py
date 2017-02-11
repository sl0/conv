#!/usr/bin/env python

#encoding:utf8

from ip6tables_converter import Chains, Tables, main as haupt
from mock import patch
import unittest
try:
    from StringIO import StringIO
except:
    from io import StringIO


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
        self.assertRaises(ValueError, filter.put_into_fgr, "-P OUTPUT FAIL")

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

        #filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        filter.put_into_fgr("-t nat -A FORWARD -j ACCEPT")
        self.assertEquals(['-A FORWARD -j ACCEPT '], filter.data["FORWARD"])

        self.assertRaises(ValueError, filter.put_into_fgr, "-t na -A INPUT")

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

        self.assertRaises(ValueError, filter.put_into_fgr, "-t inval -F")

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
        self.assertRaises(ValueError, filter.put_into_fgr, "-N INPUT")

    def test_07_insert_rule_fail(self):
        """
        Chain 07: insert a rule into an empty chain fails
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        #filter.put_into_fgr("-I INPUT -p tcp -j ACCEPT")
        self.assertRaises(ValueError, filter.put_into_fgr,
                          "-I INPUT -j ACCEPT")

    def test_08_insert_rule_fail(self):
        """
        Chain 08: insert a rule into a non_existing chain fails
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        #filter.put_into_fgr("-I INPUT -p tcp -j ACCEPT")
        self.assertRaises(ValueError, filter.put_into_fgr,
                          "-I PUT -j ACCEPT")

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
        self.assertRaises(ValueError, filter.put_into_fgr,
                          "-X INPUT")

    #def test_11_remove_nonexisting_chain(self):
    #    """
    #    try to remove a nonexisting chain
    #    """
    #    filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
    #    # following assertion removed because we always need to
    #    # remove a non existing chain, especially on runing such
    #    # genereated scripts for the very first time on a machine
    #    # so the raise is removed due to practicapability
    #    #self.assertRaises(ValueError, filter.put_into_fgr,
    #    #   "-X USERDEFCHAIN")
    #    pass

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
        self.assertRaises(ValueError, filter.put_into_fgr,
                          "-Y USERCHAIN")


class Tables_Test(unittest.TestCase):
    '''
    Tables: some first tests for the class
    '''

    def test_01_create_a_tables_object(self):
        """
        Tables 01: create a Tables object, check chains
        """
        self.assertIsInstance(Tables(""), Tables)

        tables = Tables("")
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
        tables = Tables("")
        line = "ip6tables -t nat -A PREROUTING -s 10.0.0.0/21"
        line = line + " -p tcp --dport   80 -j SNAT --to-source 192.168.1.15"
        tables.put_into_tables(line)
        expect = ['-A PREROUTING -s 10.0.0.0/21 -p tcp --dport 80 -j SNAT --to-source 192.168.1.15 ']
        self.assertEquals(expect, tables.data["nat"]["PREROUTING"])

    def test_03_mangle_table(self):
        """
        Tables 03: mangle INPUT entry
        """
        tables = Tables("")
        line = "ip6tables -t mangle -A INPUT"
        line = line + " -p tcp --dport   80 -j ACCEPT"
        tables.put_into_tables(line)
        expect = ['-A INPUT -p tcp --dport 80 -j ACCEPT ']
        self.assertEquals(expect, tables.data["mangle"]["INPUT"])

    def test_04_raw_table(self):
        """
        Tables 04: raw OUTPUT entry
        """
        tables = Tables("")
        line = "ip6tables -t raw -A OUTPUT"
        line = line + " -p tcp --dport   80 -j ACCEPT"
        tables.put_into_tables(line)
        expect = ['-A OUTPUT -p tcp --dport 80 -j ACCEPT ']
        self.assertEquals(expect, tables.data["raw"]["OUTPUT"])

    def test_05_not_existing_chain(self):
        """
        Tables 05: INPUT to not existing chain
        """
        tables = Tables("")
        line = "ip6tables -t raw -A NONEXIST"
        line = line + " -p tcp --dport   80 -j ACCEPT"
        happend = False
        try:
            self.assertRaises(ValueError, tables, tables.put_into_tables(line))
        except:
            happend = True
        self.assertEquals(happend, True)

    def test_06_read_not_existing_file(self):
        """
        Tables 06: read non existing file
        """
        filename = "not-exist-is-ok"
        happend = False
        try:
            self.assertRaises(ValueError, Tables(filename))
        except:
            happend = True
        self.assertEquals(happend, True)

    def test_07_read_empty_file(self):
        """
        Tables 07: read empty file (in relation to ip6tables-commands)
        """
        filename = "MANIFEST"
        tables = Tables(filename)
        expect = {'filter': {'FORWARD': [], 'INPUT': [], 'OUTPUT': []},
                  'raw': {'OUTPUT': [], 'PREROUTING': []},
                  'mangle': {'FORWARD': [], 'INPUT': [], 'POSTROUTING': [],
                             'PREROUTING': [], 'OUTPUT': []},
                  'nat': {'OUTPUT': [], 'PREROUTING': [], 'POSTROUTING': []}}
        self.assertEquals(expect, tables.data)

    def test_08_re6ference_one(self):
        """
        Tables 08: read default file: re6ference-one, check chains
        """
        tables = Tables("re6ference-one")
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

    def test_09_shell_variables(self):
        """
        Tables 09: read buggy file with shell variables
        """
        expect = "Line 8:"
        sys_exit_val = False
        try:
            with patch('sys.stdout', new=StringIO()) as fake_out:
                tables = Tables('test-shell-variables')
        except SystemExit:
            sys_exit_val = True
        finally:
            pass
        self.assertIn(expect, fake_out.getvalue())
        self.assertTrue(sys_exit_val)

    def test_10_shell_functions(self):
        """
        Tables 10: read buggy file with shell functions
        """
        expect = "Line 6:"
        sys_exit_val = False
        try:
            with patch('sys.stdout', new=StringIO()) as fake_out:
                tables = Tables('test-debian-bug-no-748638')
        except SystemExit:
            sys_exit_val = True
        finally:
            pass
        self.assertIn(expect, fake_out.getvalue())
        self.assertTrue(sys_exit_val)

    def test_11_re6ference_sloppy_one(self):
        """
        Tables 11: read sloppy input file: re6ference-sloppy-one, check chains
        """
        tables = Tables('re6ference-sloppy-one', True)
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

if __name__ == "__main__":
        unittest.main()
