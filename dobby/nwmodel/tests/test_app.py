#!/usr/bin/env python3

from dobby.classes.node import *
from dobby.classes.flow import *
from dobby.classes.app import *
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestNetworkApp(unittest.TestCase):
    def setUp(self):
        self.app = NetworkApp(app_name="YouTube", app_type=AppType.STREAMING_VIDEO,
                              nodes=[Node(node_name="Node1")], flows=[Flow(flow_type=FlowType.TCP)])

    def tearDown(self):
        self.app = None

    def test_validate_empty_node(self):
        self.app = NetworkApp()
        self.assertIsNone(self.app.app_name)
        self.assertEqual(self.app.app_type, AppType.UNKNOWN)
        self.assertEqual(self.app.flows, [])
        self.assertEqual(self.app.nodes, [])

    def test_validate_filled_node(self):
        self.assertEqual(self.app.app_name, "YouTube")
        self.assertEqual(self.app.app_type, AppType.STREAMING_VIDEO)
        self.assertEqual(len(self.app.flows), 1)
        self.assertEqual(len(self.app.nodes), 1)
        self.assertEqual(self.app.nodes[0].node_name, "Node1")
        self.assertEqual(self.app.flows[0].flow_type, FlowType.TCP)

    def test_validate_add_flows(self):
        self.app.add_flows(flows=[Flow(), Flow()])
        self.assertEqual(len(self.app.flows), 3)

    def test_validate_add_nodes(self):
        self.app.add_nodes(nodes=[Node()])
        self.assertEqual(len(self.app.nodes), 2)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNetworkApp)
    unittest.TextTestRunner(verbosity=2).run(suite)
