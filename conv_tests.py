#!/usr/bin/env python

#encoding:utf8

from conv import Chains, Tables, main as haupt
import unittest


class Chains_Test(unittest.TestCase):
    '''some tests for class Chain'''

    def test_01_create_a_chain_object(self):
        """
        create a Filter group, f.e. filter
        """
        self.assertIsInstance(Chains("filter", \
            ["INPUT", "FORWARD", "OUTPUT"]), Chains)
        self.assertEquals({}, Chains("filter", []))
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        self.assertEquals("filter", filter.name)
        self.assertEquals(['INPUT', 'FORWARD', 'OUTPUT'], filter.tables)
        self.assertEquals("-", filter.policy)
        self.assertEquals(0, filter.length)
        self.assertEquals( \
            {'FORWARD': 'ACCEPT', 'INPUT': 'ACCEPT', 'OUTPUT': 'ACCEPT'}, \
            filter.poli)

    def test_02_prove_policies(self):
        """
        check 3 valid policies, 1 exception
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        filter.put_into_fgr("-P INPUT DROP")
        self.assertEquals( \
            {'FORWARD': 'ACCEPT', 'INPUT': 'DROP', 'OUTPUT': 'ACCEPT'}, \
            filter.poli)
        filter.put_into_fgr("-P FORWARD REJECT")
        self.assertEquals( \
            {'FORWARD': 'REJECT', 'INPUT': 'DROP', 'OUTPUT': 'ACCEPT'}, \
            filter.poli)
        filter.put_into_fgr("-P OUTPUT DROP")
        self.assertEquals( \
            {'FORWARD': 'REJECT', 'INPUT': 'DROP', 'OUTPUT': 'DROP'}, \
            filter.poli)
        self.assertRaises(ValueError, filter.put_into_fgr, "-P OUTPUT FAIL")

    def test_03_tables_names(self):
        """
        3 cases OK, 1 Exception
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
        flush filter group, 2 rules and an invalid chain
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        filter.put_into_fgr("-t filter -A INPUT -i sl0 -j ACCEPT")
        self.assertEquals(['-A INPUT -i sl0 -j ACCEPT '], \
            filter.data["INPUT"])
        filter.put_into_fgr("-A OUTPUT -o sl1 -j ACCEPT")
        self.assertEquals(['-A OUTPUT -o sl1 -j ACCEPT'], \
            filter.data["OUTPUT"])

        filter.put_into_fgr("-F")
        self.assertEquals([], filter.data["INPUT"])
        self.assertEquals([], filter.data["OUTPUT"])

        self.assertRaises(ValueError, filter.put_into_fgr, "-t inval -F")

    def test_05_new_chain(self):
        """
        create a new chain in filtergroup,
        create an exsiting chain should fail
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        filter.put_into_fgr("-N NEWCHAIN")
        self.assertEquals( \
            {'FORWARD': [], 'INPUT': [], 'NEWCHAIN': [], 'OUTPUT': []},
            filter.data)
        self.assertRaises(ValueError, filter.put_into_fgr, "-N INPUT")

    def test_06_insert_rule_fail(self):
        """
        insert a rule into an empty chain fails
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        #filter.put_into_fgr("-I INPUT -p tcp -j ACCEPT")
        self.assertRaises(ValueError, filter.put_into_fgr,  \
            "-I INPUT -j ACCEPT")

    def test_07_insert_rule_fail(self):
        """
        insert a rule into a non_existing chain fails
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        #filter.put_into_fgr("-I INPUT -p tcp -j ACCEPT")
        self.assertRaises(ValueError, filter.put_into_fgr,  \
            "-I PUT -j ACCEPT")
    
    def test_08_insert_rule_works(self):
        """
        insert a rule into a nonempty chain works at start
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        filter.put_into_fgr("-A INPUT -p tcp -j ACCEPT")
        filter.put_into_fgr("-I INPUT -p udp -j ACCEPT")
        filter.put_into_fgr("-I INPUT -p esp -j ACCEPT")
        expect = ['-I INPUT -p esp -j ACCEPT', \
                  '-I INPUT -p udp -j ACCEPT', \
                  '-A INPUT -p tcp -j ACCEPT']
        self.assertEquals(expect, filter.data["INPUT"])

    def test_09_append_rule(self):
        """
        append a rule to a chain
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        filter.put_into_fgr("-A INPUT -p tcp -j ACCEPT")
        self.assertEquals(['-A INPUT -p tcp -j ACCEPT'], filter.data["INPUT"])
        filter.put_into_fgr("-A INPUT -p udp -j ACCEPT")
        filter.put_into_fgr("-A INPUT -p esp -j ACCEPT")
        expect = ['-A INPUT -p tcp -j ACCEPT', \
                  '-A INPUT -p udp -j ACCEPT', \
                  '-A INPUT -p esp -j ACCEPT']
        self.assertEquals(expect, filter.data["INPUT"])

    def test_10_remove_predef_chain(self):
        """
        try to remove a prefined chain
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        self.assertRaises(ValueError, filter.put_into_fgr,  \
            "-X INPUT")

    def test_11_remove_nonexisting_chain(self):
        """
        try to remove a nonexisting chain
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        self.assertRaises(ValueError, filter.put_into_fgr,  \
            "-X USERDEFCHAIN")

    def test_12_remove_chain(self):
        """
        try to remove an existing chain
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        filter.put_into_fgr("-N NEWCHAIN")
        self.assertEquals( \
            {'FORWARD': [], 'INPUT': [], 'NEWCHAIN': [], 'OUTPUT': []},
            filter.data)
        filter.put_into_fgr("-X NEWCHAIN")
        self.assertEquals( \
            {'FORWARD': [], 'INPUT': [], 'OUTPUT': []},
            filter.data)

    def test_13_illegal_command(self):
        """
        try an ilegal command
        """
        filter = Chains("filter", ["INPUT", "FORWARD", "OUTPUT"])
        self.assertRaises(ValueError, filter.put_into_fgr,  \
            "-Y USERCHAIN")


class Tables_Test(unittest.TestCase):
    '''
    Tables: some first tests for the class
    '''

    def test_01_create_a_tables_object(self):
        """
        create a Tables object, check chains
        """
        self.assertIsInstance(Tables(""), Tables)

        tables = Tables("")
        expect = {'filter': {'FORWARD': [], 'INPUT': [], 'OUTPUT': []}, \
                'raw': {'OUTPUT': [], 'PREROUTING': []}, \
                'mangle': {'FORWARD': [], 'INPUT': [], \
                    'POSTROUTING': [], 'PREROUTING': [], 'OUTPUT': []}, \
                'nat': {'OUTPUT': [], 'PREROUTING': [], 'POSTROUTING': []}}
        self.assertEquals(expect, tables.data)

    def test_02_nat_prerouting(self):
        """
        nat PREROUTING entry
        """
        tables = Tables("")
        line = "iptables -t nat -A PREROUTING -s 10.0.0.0/21"
        line = line + " -p tcp --dport   80 -j SNAT --to-source 192.168.1.15"
        tables.put_into_tables(line)
        expect = ['-A PREROUTING -s 10.0.0.0/21 -p tcp --dport 80 -j SNAT --to-source 192.168.1.15 ']
        self.assertEquals(expect, tables.data["nat"]["PREROUTING"])

    def test_03_mangle_table(self):
        """
        mangle INPUT entry
        """
        tables = Tables("")
        line = "iptables -t mangle -A INPUT"
        line = line + " -p tcp --dport   80 -j ACCEPT"
        tables.put_into_tables(line)
        expect = ['-A INPUT -p tcp --dport 80 -j ACCEPT ']
        self.assertEquals(expect, tables.data["mangle"]["INPUT"])

    def test_04_raw_table(self):
        """
        raw OUTPUT entry
        """
        tables = Tables("")
        line = "iptables -t raw -A OUTPUT"
        line = line + " -p tcp --dport   80 -j ACCEPT"
        tables.put_into_tables(line)
        expect = ['-A OUTPUT -p tcp --dport 80 -j ACCEPT ']
        self.assertEquals(expect, tables.data["raw"]["OUTPUT"])

    def test_05_not_existing_chain(self):
        """
        INPUT to not existing chain
        """
        tables = Tables("")
        line = "iptables -t raw -A INPUT"
        line = line + " -p tcp --dport   80 -j ACCEPT"
        happend = False
        try:
            self.assertRaises(ValueError, tables, put_into_tables(), line)
        except:
            happend = True
        self.assertEquals(happend, True)
    
    def test_06_read_not_existing_file(self):
        """
        read non existing file
        """
        filename = "not-exist-ist-ok"
        happend = False
        try:
            self.assertRaises(ValueError, Tables(), filename)
        except:
            happend = True
        self.assertEquals(happend, True)


    def test_07_reference_one(self):
        """
        read default file: reference-one, check chains
        """
        tables = Tables()
        expect = { \
            'filter': {'FORWARD': [], \
                'INPUT': ['-A INPUT -p tcp --dport 23 -j ACCEPT '], \
                'USER_CHAIN': ['-A USER_CHAIN -p icmp -j DROP '], \
                'OUTPUT': []}, \
            'raw': {'OUTPUT': [], 'PREROUTING': []}, \
            'mangle': {'FORWARD': [], 'INPUT': [], 'POSTROUTING': [],  \
                'PREROUTING': [], 'OUTPUT': []}, \
            'nat': {'OUTPUT': [], \
                'POSTROUTING': ['-A POSTROUTING -s 10.0.0.0/21 -p tcp --dport 80 -j SNAT --to-source 192.168.1.15 '],
                'PREROUTING': ['-A PREROUTING -d 192.0.2.5/32 -p tcp --dport 443 -j DNAT --to-destination 10.0.0.5:1500 ']}}
        self.maxDiff = None
        self.assertEquals(expect, tables.data)
        tables.table_printout()

    def test_08_main(self):
        """
        procedure main
        """
        try:
            helper = True
            self.assertAlmostEquals("nosetests: -v", haupt, "-h")
        except:
            helper = False
        self.assertEquals(helper, False)

if __name__ == "__main__":
        unittest.main()
