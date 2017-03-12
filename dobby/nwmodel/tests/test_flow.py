#!/usr/bin/env python3

import dobby.nwmodel.phymodel as phymodel
import dobby.nwmodel.endpoint as endpoint
import dobby.nwmodel.node as node
import dobby.nwmodel.flow as flow
import dobby.nwmodel.ipinfo as ipinfo
import dobby.nwmetrics.metrics as metrics
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestFlow(unittest.TestCase):
    def setUp(self):
        self.mac1 = phymodel.PhysicalAddress(phy_address='AA:BB:CC:DD:EE:FF')
        self.mac2 = phymodel.PhysicalAddress(phy_address='11:22:33:44:55:66')
        self.ipinfo1 = ipinfo.IPInfo(ipv4address='192.168.1.10')
        self.ipinfo2 = ipinfo.IPInfo(ipv4address='243.135.5.190')
        self.sport = 100
        self.dport = 200
        self.rtt_stats = metrics.Stats(min_val=1, max_val=5, var_val=2, num_samples=10)
        self.semirtt_stats1 = metrics.Stats(min_val=1, max_val=2, var_val=2, num_samples=5)
        self.semirtt_stats2 = metrics.Stats(min_val=1, max_val=7, var_val=2, num_samples=5)
        self.endpoint1 = endpoint.EndPoint(phy_address=self.mac1, ip_info=self.ipinfo1)
        self.endpoint2 = endpoint.EndPoint(phy_address=self.mac2, ip_info=self.ipinfo2)
        self.flow_metrics = metrics.TCPMetrics(start_ts=1, end_ts=2, total_pkts=10, total_bytes=10,
                                       total_acks=4, total_loss=2, mtu=1200,
                                       rtt_stats=self.rtt_stats)
        self.flow_metrics_src_to_dst = metrics.TCPMetrics(start_ts=1, end_ts=2, total_pkts=5, total_bytes=10,
                                       total_acks=4, total_loss=2, mtu=1200,
                                       rtt_stats=self.semirtt_stats1)
        self.flow_metrics_dst_to_src = metrics.TCPMetrics(start_ts=1, end_ts=2, total_pkts=4, total_bytes=10,
                                       total_acks=4, total_loss=2, mtu=1200,
                                       rtt_stats=self.semirtt_stats2)
        self.flow = flow.Flow(edge_list=[(self.endpoint1, self.endpoint2)],
                         src_endpoint=self.endpoint1,
                         dst_endpoint=self.endpoint2,
                         sport=self.sport,
                         dport=self.dport,
                         flow_type=flow.FlowType.TCP,
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
        self.assertEqual(self.flow.flow_type, flow.FlowType.TCP)
        self.assertEqual(self.flow.flow_metrics.total_pkts, 10)
        self.assertEqual(self.flow.flow_metrics_src_to_dst.total_pkts, 5)
        self.assertEqual(self.flow.flow_metrics_dst_to_src.total_pkts, 4)

    def test_validate_input_by_kwargs(self):
        test_input = dict(edge_list=[(self.endpoint1, self.endpoint2)],
                         src_endpoint=self.endpoint1,
                         dst_endpoint=self.endpoint2,
                         sport=self.sport,
                         dport=self.dport,
                         flow_type=flow.FlowType.TCP,
                         flow_metrics=self.flow_metrics,
                         flow_metrics_src_to_dst=self.flow_metrics_src_to_dst,
                         flow_metrics_dst_to_src=self.flow_metrics_dst_to_src)
        self.flow = flow.Flow(**test_input)
        self.assertEqual(self.flow.src_endpoint, self.endpoint1)
        self.assertEqual(self.flow.dst_endpoint, self.endpoint2)
        self.assertEqual(self.flow.sport, self.sport)
        self.assertEqual(self.flow.dport, self.dport)
        self.assertEqual(self.flow.flow_type, flow.FlowType.TCP)
        self.assertEqual(self.flow.flow_metrics.total_pkts, 10)
        self.assertEqual(self.flow.flow_metrics_src_to_dst.total_pkts, 5)
        self.assertEqual(self.flow.flow_metrics_dst_to_src.total_pkts, 4)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFlow)
    unittest.TextTestRunner(verbosity=2).run(suite)
