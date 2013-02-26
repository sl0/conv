#!/usr/bin/env python

#encoding:utf8

#from iptables_optimizer import extract_pkt_cntr, Chain, Filter
from conv import Chains
import unittest


class Chains_Test(unittest.TestCase):
    '''some first tests for class Chain'''

    def test_01_chains_object(self):
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

    def test_02_prove_policy(self):
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
        filter.put_into_fgr("-P OUTPUT NONSENSE")
        #self.assertRaises(filter, ValueError("try to set illegal policy"))
        self.assertRaises(Filter(filter, ValueError("try to set illegal policy")))


if __name__ == "__main__":
        unittest.main()
