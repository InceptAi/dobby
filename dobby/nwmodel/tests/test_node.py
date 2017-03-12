#!/usr/bin/env python3

import dobby.nwmodel.phymodel as phymodel
import dobby.nwmodel.endpoint as endpoint
import dobby.nwmodel.node as node
import dobby.nwmodel.flow as flow
import dobby.nwmodel.ipinfo as ipinfo
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestNode(unittest.TestCase):
    def setUp(self):
        self.mac = phymodel.PhysicalAddress(phy_address='AA:BB:CC:DD:EE:FF')
        self.phy_model = phymodel.WifiPhysicalModel(mac=self.mac)
        self.ip_info = ipinfo.IPInfo(ipv4address='192.168.1.1')
        self.node_id = '123456'
        self.endpoint = endpoint.EndPoint(phy_address=self.mac, ip_info=self.ip_info)
        self.node = node.Node(endpoints=[self.endpoint],
                         node_type=node.NodeType.WIRELESS_ROUTER,
                         node_name='Node1')

    def tearDown(self):
        self.node = None

    def test_validate_empty_node(self):
        self.node = node.Node()
        self.assertIsNotNone(self.node.node_id)
        self.assertIsNone(self.node.node_name)
        self.assertEqual(self.node.node_type, node.NodeType.UNKNOWN)
        self.assertEqual(len(self.node.endpoints), 0)
        self.assertEqual(len(self.node.apps), 0)
        self.assertEqual(len(self.node.flows), 0)

    def test_validate_filled_node(self):
        self.assertEqual(self.node.endpoints[0].phy_address, self.mac)
        self.assertEqual(self.node.endpoints[0].ip_info, self.ip_info)
        self.assertEqual(self.node.node_name, 'Node1')
        self.assertIsNotNone(self.node.node_id)
        self.assertEqual(self.node.node_type, node.NodeType.WIRELESS_ROUTER)

    def test_validate_add_endpoints(self):
        self.node.add_endpoints(endpoints=[endpoint.EndPoint(), endpoint.EndPoint()])
        self.assertEqual(len(self.node.endpoints), 3)

    def test_validate_add_flows(self):
        self.node.add_flows(flows=[flow.Flow(), flow.Flow()])
        self.assertEqual(len(self.node.flows), 2)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNode)
    unittest.TextTestRunner(verbosity=2).run(suite)
