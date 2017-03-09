#!/usr/bin/env python3

from dobby.classes.endpoint import *
from dobby.classes.phymodel import *
from dobby.classes.node import *
from dobby.classes.ipinfo import *
from dobby.classes.edge import *
from dobby.classes.metrics import *
from dobby.classes.flow import *
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestFlow(unittest.TestCase):
    def setUp(self):
        self.mac1 = PhysicalAddress(phy_address='AA:BB:CC:DD:EE:FF')
        self.mac2 = PhysicalAddress(phy_address='11:22:33:44:55:66')
        self.ipinfo1 = IPInfo(ipv4address='192.168.1.10')
        self.ipinfo2 = IPInfo(ipv4address='243.135.5.190')
        self.sport = 100
        self.dport = 200
        self.rtt_stats = Stats(min_val=1, max_val=5, var_val=2, num_samples=10)
        self.semirtt_stats1 = Stats(min_val=1, max_val=2, var_val=2, num_samples=5)
        self.semirtt_stats2 = Stats(min_val=1, max_val=7, var_val=2, num_samples=5)
        self.endpoint1 = EndPoint(phy_address=self.mac1, ip_info=self.ipinfo1)
        self.endpoint2 = EndPoint(phy_address=self.mac2, ip_info=self.ipinfo2)
        self.flow_metrics = TCPMetrics(start_ts=1, end_ts=2, total_pkts=10, total_bytes=10,
                                       total_acks=4, total_loss=2, mtu=1200,
                                       rtt_stats=self.rtt_stats)
        self.flow_metrics_src_to_dst = TCPMetrics(start_ts=1, end_ts=2, total_pkts=5, total_bytes=10,
                                       total_acks=4, total_loss=2, mtu=1200,
                                       rtt_stats=self.semirtt_stats1)
        self.flow_metrics_dst_to_src = TCPMetrics(start_ts=1, end_ts=2, total_pkts=4, total_bytes=10,
                                       total_acks=4, total_loss=2, mtu=1200,
                                       rtt_stats=self.semirtt_stats2)
        self.flow = Flow(edge_list=[(self.endpoint1, self.endpoint2)],
                         src_endpoint=self.endpoint1,
                         dst_endpoint=self.endpoint2,
                         sport=self.sport,
                         dport=self.dport,
                         flow_type=FlowType.TCP,
                         flow_metrics=self.flow_metrics,
                         flow_metrics_src_to_dst=self.flow_metrics_src_to_dst,
                         flow_metrics_dst_to_src=self.flow_metrics_dst_to_src)

    def tearDown(self):
        self.flow = None

    def test_validate_filled_endpoint(self):
        self.assertEqual(self.flow.src_endpoint, self.endpoint1)
        self.assertEqual(self.flow.dst_endpoint, self.endpoint2)
        self.assertEqual(self.flow.sport, self.sport)
        self.assertEqual(self.flow.dport, self.dport)
        self.assertEqual(self.flow.flow_type, FlowType.TCP)
        self.assertEqual(self.flow.flow_metrics.total_pkts, 10)
        self.assertEqual(self.flow.flow_metrics_src_to_dst.total_pkts, 5)
        self.assertEqual(self.flow.flow_metrics_dst_to_src.total_pkts, 4)

    def test_validate_input_by_kwargs(self):
        test_input = dict(edge_list=[(self.endpoint1, self.endpoint2)],
                         src_endpoint=self.endpoint1,
                         dst_endpoint=self.endpoint2,
                         sport=self.sport,
                         dport=self.dport,
                         flow_type=FlowType.TCP,
                         flow_metrics=self.flow_metrics,
                         flow_metrics_src_to_dst=self.flow_metrics_src_to_dst,
                         flow_metrics_dst_to_src=self.flow_metrics_dst_to_src)
        self.flow = Flow(**test_input)
        self.assertEqual(self.flow.src_endpoint, self.endpoint1)
        self.assertEqual(self.flow.dst_endpoint, self.endpoint2)
        self.assertEqual(self.flow.sport, self.sport)
        self.assertEqual(self.flow.dport, self.dport)
        self.assertEqual(self.flow.flow_type, FlowType.TCP)
        self.assertEqual(self.flow.flow_metrics.total_pkts, 10)
        self.assertEqual(self.flow.flow_metrics_src_to_dst.total_pkts, 5)
        self.assertEqual(self.flow.flow_metrics_dst_to_src.total_pkts, 4)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFlow)
    unittest.TextTestRunner(verbosity=2).run(suite)
