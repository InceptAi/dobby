#!/usr/bin/env python3
import dobby.nwmodel.app as networkapp
import dobby.nwmodel.node as node
import dobby.nwmodel.flow as flow
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestNetworkApp(unittest.TestCase):
    def setUp(self):
        self.networkapp = networkapp.NetworkApp(app_name="YouTube", app_type=networkapp.NetworkAppType.STREAMING_VIDEO,
                              nodes=[node.Node(node_name="Node1")], flows=[flow.Flow(flow_type=flow.FlowType.TCP)])

    def tearDown(self):
        self.networkapp = None

    def test_validate_empty_node(self):
        self.networkapp = networkapp.NetworkApp()
        self.assertIsNone(self.networkapp.app_name)
        self.assertEqual(self.networkapp.app_type, networkapp.NetworkAppType.UNKNOWN)
        self.assertEqual(self.networkapp.flows, [])
        self.assertEqual(self.networkapp.nodes, [])

    def test_validate_filled_node(self):
        self.assertEqual(self.networkapp.app_name, "YouTube")
        self.assertEqual(self.networkapp.app_type, networkapp.NetworkAppType.STREAMING_VIDEO)
        self.assertEqual(len(self.networkapp.flows), 1)
        self.assertEqual(len(self.networkapp.nodes), 1)
        self.assertEqual(self.networkapp.nodes[0].node_name, "Node1")
        self.assertEqual(self.networkapp.flows[0].flow_type, flow.FlowType.TCP)

    def test_validate_add_flows(self):
        self.networkapp.add_flows(flows=[flow.Flow(), flow.Flow()])
        self.assertEqual(len(self.networkapp.flows), 3)

    def test_validate_add_nodes(self):
        self.networkapp.add_nodes(nodes=[node.Node()])
        self.assertEqual(len(self.networkapp.nodes), 2)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNetworkApp)
    unittest.TextTestRunner(verbosity=2).run(suite)
