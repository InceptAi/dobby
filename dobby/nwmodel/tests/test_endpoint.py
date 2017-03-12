#!/usr/bin/env python3

import dobby.nwmodel.endpoint as endpoint
import dobby.nwmodel.phymodel as phymodel
import dobby.nwmodel.node as node
import dobby.nwmodel.ipinfo as ipinfo
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestEndPoint(unittest.TestCase):
    def setUp(self):
        self.mac = phymodel.PhysicalAddress(phy_address='AA:BB:CC:DD:EE:FF')
        self.phy_model = phymodel.WifiPhysicalModel(mac=self.mac)
        self.ip_info = ipinfo.IPInfo(ipv4address='192.168.1.1')
        self.node_id = '123456'
        self.endpoint = endpoint.EndPoint()

    def tearDown(self):
        self.endpoint = None

    def test_validate_empty_endpoint(self):
        self.assertIsNone(self.endpoint.phy_address)
        self.assertIsNone(self.endpoint.phy_model)
        self.assertIsNone(self.endpoint.node_id)
        self.assertIsNone(self.endpoint.ip_info)

    def test_validate_filled_endpoint(self):
        self.endpoint = endpoint.EndPoint(phy_address=self.mac, ip_info=self.ip_info,
                                          phy_model=self.phy_model, node_id=self.node_id)
        self.assertEqual(self.endpoint.phy_address, self.mac)
        self.assertEqual(self.endpoint.ip_info, self.ip_info)
        self.assertEqual(self.endpoint.node_id, self.node_id)
        self.assertEqual(self.endpoint.phy_model, self.phy_model)

    def test_validate_endpoint_physical_addr(self):
        self.endpoint = endpoint.EndPoint(phy_address=self.mac)
        self.assertEqual(self.endpoint.phy_address, self.mac)

    def test_validate_input_by_kwargs(self):
        test_input = dict(phy_address=self.mac)
        self.endpoint = endpoint.EndPoint(**test_input)
        self.assertEqual(self.endpoint.phy_address, self.mac)

    def test_validate_endpoint_with_ip_info(self):
        self.endpoint = endpoint.EndPoint(ip_info=self.ip_info)
        self.assertEqual(self.endpoint.ip_info, self.ip_info)

    def test_validate_update_ip_info(self):
        self.endpoint.update_ip_info(ip_info=self.ip_info)
        self.assertEqual(self.endpoint.ip_info, self.ip_info)

    def test_validate_update_phy_model(self):
        self.endpoint.update_phy_model(phy_model=self.phy_model)
        self.assertEqual(self.endpoint.phy_model, self.phy_model)

    def test_validate_update_phy_model(self):
        self.endpoint.update_phy_model(phy_model=self.phy_model)
        self.assertEqual(self.endpoint.phy_model, self.phy_model)

    def test_validate_update_node_info(self):
        self.endpoint.update_node_info(node_id=self.node_id)
        self.assertEqual(self.endpoint.node_id, self.node_id)

    def test_validate_update_mac_info(self):
        self.endpoint.update_phy_address(phy_address=self.mac)
        self.assertEqual(self.endpoint.phy_address, self.mac)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEndPoint)
    unittest.TextTestRunner(verbosity=2).run(suite)
