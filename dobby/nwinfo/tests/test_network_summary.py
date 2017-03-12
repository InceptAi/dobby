#!/usr/bin/env python3

import dobby.nwmodel.phymodel as phymodel
import dobby.nwmodel.endpoint as endpoint
import dobby.nwmodel.edge as edge
import dobby.nwmodel.node as node
import dobby.nwmodel.flow as flow
import dobby.nwmodel.ipinfo as ipinfo
import dobby.nwmodel.app as networkapp
import dobby.nwinfo.networksummary as networksummary
import unittest
__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestNetworkSummary(unittest.TestCase):
    def setUp(self):
        self.mac = phymodel.PhysicalAddress(phy_address='AA:BB:CC:DD:EE:FF')
        self.mac2 = phymodel.PhysicalAddress(phy_address='11:22:33:44:55:66')
        self.phy_model = phymodel.WifiPhysicalModel(mac=self.mac)
        self.ip_info = ipinfo.IPInfo(ipv4address='192.168.1.1')
        self.node_id = '123456'
        self.endpoint = endpoint.EndPoint(phy_address=self.mac, ip_info=self.ip_info)
        self.endpoint2 = endpoint.EndPoint(phy_address=self.mac2)
        self.edge = edge.Edge(endpoint_a=self.endpoint,
                              endpoint_b=self.endpoint2,
                              edge_type=edge.EdgeType.PHYSICAL)
        self.node = node.Node(endpoints=[self.endpoint],
                                  node_type=node.NodeType.WIRELESS_ROUTER,
                                  node_name='Node1')
        self.flow = flow.Flow(flow_type=flow.FlowType.TCP)
        self.networkapp = networkapp.NetworkApp(app_name="YouTube",
                                                app_type=networkapp.NetworkAppType.STREAMING_VIDEO,
                                                nodes=[self.node],
                                                flows=[self.flow])
        self.ns = networksummary.NetworkSummary(start_ts=1, end_ts=2,
                                                mac_to_endpoints={str(self.mac):self.endpoint,
                                                                  str(self.mac2):self.endpoint2},
                                                ip_to_endpoints={str(self.ip_info.ipv4address):
                                                                     self.endpoint},
                                                nodes={'a':self.node},
                                                edges={'b':self.edge},
                                                ip_flows={'c':self.flow},
                                                apps={'d':self.networkapp},
                                                phy_models={'e':self.phy_model})


    def tearDown(self):
        self.ns = None

    def test_network_summary_is_correctly_instantiated(self):
        self.assertEqual(self.ns.start_ts, 1)
        self.assertEqual(self.ns.end_ts, 2)
        self.assertDictEqual(self.ns.mac_to_endpoints,
                             {'aa:bb:cc:dd:ee:ff':self.endpoint, '11:22:33:44:55:66':self.endpoint2})
        self.assertDictEqual(self.ns.ip_to_endpoints, {'192.168.1.1':self.endpoint})
        self.assertListEqual(list(self.ns.nodes.values()), [self.node])
        self.assertListEqual(list(self.ns.edges.values()), [self.edge])
        self.assertListEqual(list(self.ns.ip_flows.values()), [self.flow])
        self.assertListEqual(list(self.ns.apps.values()), [self.networkapp])
        self.assertListEqual(list(self.ns.phy_models.values()), [self.phy_model])

    def test_empty_network_summary_is_correctly_instantiated(self):
        self.ns = networksummary.NetworkSummary()
        self.assertIsNone(self.ns.start_ts)
        self.assertIsNone(self.ns.end_ts)
        self.assertDictEqual(self.ns.mac_to_endpoints, {})
        self.assertDictEqual(self.ns.ip_to_endpoints, {})
        self.assertDictEqual(self.ns.nodes, {})
        self.assertDictEqual(self.ns.edges, {})
        self.assertDictEqual(self.ns.ip_flows, {})
        self.assertDictEqual(self.ns.apps, {})
        self.assertDictEqual(self.ns.phy_models, {})

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNetworkSummary)
    unittest.TextTestRunner(verbosity=2).run(suite)
