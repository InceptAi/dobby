#!/usr/bin/env python3

import dobby.nwmodel.phymodel as phymodel
import dobby.nwmodel.endpoint as endpoint
import dobby.nwmodel.edge as edge
import dobby.nwmodel.node as node
import dobby.nwmodel.flow as flow
import dobby.nwmodel.ipinfo as ipinfo
import dobby.nwmetrics.metrics as metrics
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestEdge(unittest.TestCase):
    def setUp(self):
        self.mac1 = phymodel.PhysicalAddress(phy_address='AA:BB:CC:DD:EE:FF')
        self.mac2 = phymodel.PhysicalAddress(phy_address='11:22:33:44:55:66')
        self.endpoint1 = endpoint.EndPoint(phy_address=self.mac1)
        self.endpoint2 = endpoint.EndPoint(phy_address=self.mac2)
        self.metrics_undirected = metrics.Metrics(start_ts=1, end_ts=2, total_pkts=1, total_bytes=10)
        self.metrics_ab = metrics.Metrics(start_ts=1, end_ts=2, total_pkts=0, total_bytes=0)
        self.metrics_ba = metrics.Metrics(start_ts=1, end_ts=2, total_pkts=1, total_bytes=10)
        self.edge = edge.Edge(endpoint_a=self.endpoint1,
                         endpoint_b=self.endpoint2,
                         edge_type=edge.EdgeType.PHYSICAL)

    def tearDown(self):
        self.edge = None

    def test_validate_filled_endpoint(self):
        self.assertEqual(self.edge.endpoint_a, self.endpoint1)
        self.assertEqual(self.edge.endpoint_b, self.endpoint2)
        self.assertEqual(self.edge.edge_type, edge.EdgeType.PHYSICAL)

    def test_validate_input_by_kwargs(self):
        test_input = dict(endpoint_a=self.endpoint1,
                          endpoint_b=self.endpoint2,
                          edge_type=edge.EdgeType.PHYSICAL)
        self.edge = edge.Edge(**test_input)
        self.assertEqual(self.edge.endpoint_a, self.endpoint1)
        self.assertEqual(self.edge.endpoint_b, self.endpoint2)
        self.assertEqual(self.edge.edge_type, edge.EdgeType.PHYSICAL)

    def test_default_edge_type_is_unknown(self):
        test_input = dict(endpoint_a=self.endpoint1,
                          endpoint_b=self.endpoint2)
        self.edge = edge.Edge(**test_input)
        self.assertEqual(self.edge.endpoint_a, self.endpoint1)
        self.assertEqual(self.edge.endpoint_b, self.endpoint2)
        self.assertEqual(self.edge.edge_type, edge.EdgeType.UNKNOWN)

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
