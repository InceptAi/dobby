#!/usr/bin/env python3

from dobby.classes.endpoint import *
from dobby.classes.phymodel import *
from dobby.classes.node import *
from dobby.classes.ipinfo import *
from dobby.classes.edge import *
from dobby.classes.metrics import *
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestEdge(unittest.TestCase):
    def setUp(self):
        self.mac1 = PhysicalAddress(phy_address='AA:BB:CC:DD:EE:FF')
        self.mac2 = PhysicalAddress(phy_address='11:22:33:44:55:66')
        self.endpoint1 = EndPoint(phy_address=self.mac1)
        self.endpoint2 = EndPoint(phy_address=self.mac2)
        self.metrics_undirected = Metrics(start_ts=1, end_ts=2, total_pkts=1, total_bytes=10)
        self.metrics_ab = Metrics(start_ts=1, end_ts=2, total_pkts=0, total_bytes=0)
        self.metrics_ba = Metrics(start_ts=1, end_ts=2, total_pkts=1, total_bytes=10)
        self.edge = Edge(endpoint_a=self.endpoint1,
                         endpoint_b=self.endpoint2,
                         edge_type=EdgeType.PHYSICAL)

    def tearDown(self):
        self.edge = None

    def test_validate_filled_endpoint(self):
        self.assertEqual(self.edge.endpoint_a, self.endpoint1)
        self.assertEqual(self.edge.endpoint_b, self.endpoint2)
        self.assertEqual(self.edge.edge_type, EdgeType.PHYSICAL)

    def test_validate_input_by_kwargs(self):
        test_input = dict(endpoint_a=self.endpoint1,
                          endpoint_b=self.endpoint2,
                          edge_type=EdgeType.PHYSICAL)
        self.edge = Edge(**test_input)
        self.assertEqual(self.edge.endpoint_a, self.endpoint1)
        self.assertEqual(self.edge.endpoint_b, self.endpoint2)
        self.assertEqual(self.edge.edge_type, EdgeType.PHYSICAL)

    def test_default_edge_type_is_unknown(self):
        test_input = dict(endpoint_a=self.endpoint1,
                          endpoint_b=self.endpoint2)
        self.edge = Edge(**test_input)
        self.assertEqual(self.edge.endpoint_a, self.endpoint1)
        self.assertEqual(self.edge.endpoint_b, self.endpoint2)
        self.assertEqual(self.edge.edge_type, EdgeType.UNKNOWN)

    def test_update_undirected_metrics(self):
        self.edge.update_undirected_metrics(metrics=self.metrics_undirected)
        self.assertEqual(self.edge.edge_metrics.total_pkts, 1)
        self.assertEqual(self.edge.edge_metrics.total_bytes, 10)

    def test_update_metrics_ab(self):
        self.edge.update_metrics_ab(metrics_ab=self.metrics_ab)
        self.assertEqual(self.edge.edge_metrics_ab.total_pkts, 0)
        self.assertEqual(self.edge.edge_metrics_ab.total_bytes, 0)

    def test_update_metrics_ba(self):
        self.edge.update_metrics_ba(metrics_ba=self.metrics_ba)
        self.assertEqual(self.edge.edge_metrics_ba.total_pkts, 1)
        self.assertEqual(self.edge.edge_metrics_ba.total_bytes, 10)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEdge)
    unittest.TextTestRunner(verbosity=2).run(suite)
