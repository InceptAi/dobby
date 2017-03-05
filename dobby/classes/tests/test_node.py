#!/usr/bin/env python3

from dobby.classes.endpoint import *
from dobby.classes.phymodel import *
from dobby.classes.node import *
from dobby.classes.ipinfo import *
from dobby.classes.flow import *
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestNode(unittest.TestCase):
    def setUp(self):
        self.mac = PhysicalAddress(phy_address='AA:BB:CC:DD:EE:FF')
        self.phy_model = WifiPhysicalModel(mac=self.mac)
        self.ip_info = IPInfo(ipv4address='192.168.1.1')
        self.node_id = '123456'
        self.endpoint = EndPoint(phy_address=self.mac, ip_info=self.ip_info)
        self.node = Node(endpoints=[self.endpoint],
                         node_type=NodeType.WIRELESS_ROUTER,
                         node_name='Node1')

    def tearDown(self):
        self.node = None

    def test_validate_empty_node(self):
        self.node = Node()
        self.assertIsNotNone(self.node.node_id)
        self.assertIsNone(self.node.node_name)
        self.assertEqual(self.node.node_type, NodeType.UNKNOWN)
        self.assertEqual(len(self.node.endpoints), 0)
        self.assertEqual(len(self.node.apps), 0)
        self.assertEqual(len(self.node.flows), 0)

    def test_validate_filled_node(self):
        self.assertEqual(self.node.endpoints[0].phy_address, self.mac)
        self.assertEqual(self.node.endpoints[0].ip_info, self.ip_info)
        self.assertEqual(self.node.node_name, 'Node1')
        self.assertIsNotNone(self.node.node_id)
        self.assertEqual(self.node.node_type, NodeType.WIRELESS_ROUTER)

    def test_validate_add_endpoints(self):
        self.node.add_endpoints(endpoints=[EndPoint(), EndPoint()])
        self.assertEqual(len(self.node.endpoints), 3)

    def test_validate_add_flows(self):
        self.node.add_flows(flows=[Flow(), Flow()])
        self.assertEqual(len(self.node.flows), 2)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNode)
    unittest.TextTestRunner(verbosity=2).run(suite)
