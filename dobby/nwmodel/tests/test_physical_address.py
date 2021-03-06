#!/usr/bin/env python3

import dobby.nwmodel.phymodel as phymodel
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestPhysicalAddress(unittest.TestCase):
    def setUp(self):
        self.phy_address = phymodel.PhysicalAddress(phy_address='AA:BB:CC:DD:EE:FF')

    def test_correct_physical_address_is_accepted(self):
        self.assertEqual(str(self.phy_address), 'aa:bb:cc:dd:ee:ff')

    def test_equal_works_on_physical_address(self):
        self.assertEqual(self.phy_address, phymodel.PhysicalAddress(phy_address='AA:BB:CC:DD:EE:FF'))

    def test_physical_address_is_case_insensitive(self):
        self.assertEqual(self.phy_address, phymodel.PhysicalAddress(phy_address='aa:bb:cc:dd:ee:ff'))

    def test_not_equal_works_on_physical_address(self):
        self.assertNotEqual(self.phy_address, phymodel.PhysicalAddress(phy_address='11:BB:CC:DD:EE:FF'))

    def test_incorrect_physical_address_returns_none(self):
        self.assertIsNone(phymodel.PhysicalAddress().phy_address)
        self.assertIsNone(phymodel.PhysicalAddress('AA:BB:CC').phy_address)

    def test_passing_arguments_with_dict_works(self):
        input_dict = dict(phy_address='AA:BB:CC:DD:EE:FF')
        self.phy_address = phymodel.PhysicalAddress(**input_dict)
        self.assertEqual(str(self.phy_address), 'aa:bb:cc:dd:ee:ff')

    def test_updating_vendor_works(self):
        new_vendor = 'foo'
        self.phy_address.update_vendor(new_vendor)
        self.assertEqual(self.phy_address.vendor, new_vendor)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPhysicalAddress)
    unittest.TextTestRunner(verbosity=2).run(suite)
