#!/usr/bin/env python3

from dobby.classes.metrics import *
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestTCPMetrics(unittest.TestCase):
    def setUp(self):
        self.rtt_stats = Stats(min_val=10.254, max_val=120.001, num_samples=10)
        self.tcp_metric = TCPMetrics(start_ts=1, end_ts=2, total_pkts=10, total_bytes=100,
                                     duration=1, mtu=1200, total_loss=5,
                                     total_acks=10, rtt_stats=self.rtt_stats)

    def tearDown(self):
        self.tcp_metric = None

    def test_validate_tcp_metric(self):
        self.assertEqual(self.tcp_metric.total_pkts, 10)
        self.assertEqual(self.tcp_metric.total_bytes, 100)
        self.assertEqual(self.tcp_metric.total_loss, 5)
        self.assertEqual(self.tcp_metric.mtu, 1200)
        self.assertEqual(self.tcp_metric.duration, 1)
        self.assertEqual(self.tcp_metric.total_acks, 10)
        #rtt stats
        self.assertEqual(self.tcp_metric.rtt_stats.min_val, 10.254)
        self.assertEqual(self.tcp_metric.rtt_stats.max_val, 120.001)
        self.assertEqual(self.tcp_metric.rtt_stats.num_samples, 10)

    def test_validate_input_by_kwargs(self):
        test_input = dict(start_ts=1, end_ts=2, total_pkts=10, total_bytes=100,
                                     duration=1, mtu=1200, total_loss=5,
                                     total_acks=10, rtt_stats=self.rtt_stats)
        self.edge = TCPMetrics(**test_input)
        self.assertEqual(self.tcp_metric.total_pkts, 10)
        self.assertEqual(self.tcp_metric.total_bytes, 100)
        self.assertEqual(self.tcp_metric.total_loss, 5)
        self.assertEqual(self.tcp_metric.mtu, 1200)
        self.assertEqual(self.tcp_metric.duration, 1)
        self.assertEqual(self.tcp_metric.total_acks, 10)
        #rtt stats
        self.assertEqual(self.tcp_metric.rtt_stats.min_val, 10.254)
        self.assertEqual(self.tcp_metric.rtt_stats.max_val, 120.001)
        self.assertEqual(self.tcp_metric.rtt_stats.num_samples, 10)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTCPMetrics)
    unittest.TextTestRunner(verbosity=2).run(suite)
