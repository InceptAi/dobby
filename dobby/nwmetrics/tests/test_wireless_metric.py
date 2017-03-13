#!/usr/bin/env python3

import dobby.nwmetrics.metrics as metrics
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestWirelessMetrics(unittest.TestCase):
    def setUp(self):
        self.snr_stats = metrics.Stats(min_val=-90, max_val=-10, num_samples=10)
        self.rate_stats = metrics.Stats(percentile_10=2, percentile_90=48, percentile_50=24, num_samples=10)
        self.wireless_metric = metrics.WirelessMetrics(start_ts=1, end_ts=2, total_pkts=10, total_bytes=100,
                                               total_data_pkts=1, total_data_bytes=20, total_retx=1,
                                               total_trans_time_usec=100, avg_data_pkt_duration_usec=10,
                                               snr_stats=self.snr_stats, rate_stats=self.rate_stats)

    def tearDown(self):
        self.wireless_metric = None

    def test_validate_wireless_metric(self):
        self.assertEqual(self.wireless_metric.total_pkts, 10)
        self.assertEqual(self.wireless_metric.total_bytes, 100)
        self.assertEqual(self.wireless_metric.total_data_pkts, 1)
        self.assertEqual(self.wireless_metric.total_data_bytes, 20)
        self.assertEqual(self.wireless_metric.total_retx, 1)
        self.assertEqual(self.wireless_metric.total_trans_time_usec, 100)
        self.assertEqual(self.wireless_metric.avg_data_pkt_duration_usec, 10)
        #rssi stats
        self.assertEqual(self.wireless_metric.snr_stats.min_val, -90)
        self.assertEqual(self.wireless_metric.snr_stats.max_val, -10)
        #rssi stats
        self.assertEqual(self.wireless_metric.rate_stats.percentile_10, 2)
        self.assertEqual(self.wireless_metric.rate_stats.percentile_50, 24)
        self.assertEqual(self.wireless_metric.rate_stats.percentile_90, 48)


    def test_validate_input_by_kwargs(self):
        self.wireless_metric = None
        test_input = dict(start_ts=1, end_ts=2, total_pkts=10, total_bytes=100,
                                               total_data_pkts=1, total_data_bytes=20, total_retx=1,
                                               total_trans_time_usec=100, avg_data_pkt_duration_usec=10,
                                               snr_stats=self.snr_stats, rate_stats=self.rate_stats)
        self.wireless_metric = metrics.WirelessMetrics(**test_input)
        self.assertEqual(self.wireless_metric.total_pkts, 10)
        self.assertEqual(self.wireless_metric.total_bytes, 100)
        self.assertEqual(self.wireless_metric.total_data_pkts, 1)
        self.assertEqual(self.wireless_metric.total_data_bytes, 20)
        self.assertEqual(self.wireless_metric.total_retx, 1)
        self.assertEqual(self.wireless_metric.total_trans_time_usec, 100)
        self.assertEqual(self.wireless_metric.avg_data_pkt_duration_usec, 10)
        #rssi stats
        self.assertEqual(self.wireless_metric.snr_stats.min_val, -90)
        self.assertEqual(self.wireless_metric.snr_stats.max_val, -10)
        self.assertEqual(self.wireless_metric.snr_stats.num_samples, 10)
        #rssi stats
        self.assertEqual(self.wireless_metric.rate_stats.percentile_10, 2)
        self.assertEqual(self.wireless_metric.rate_stats.percentile_50, 24)
        self.assertEqual(self.wireless_metric.rate_stats.percentile_90, 48)
        self.assertEqual(self.wireless_metric.rate_stats.num_samples, 10)

    def test_eq_works(self):
        input_dict = dict(start_ts=1, end_ts=2, total_pkts=10, total_bytes=100,
                          total_data_pkts=1, total_data_bytes=20, total_retx=1,
                          total_trans_time_usec=100, avg_data_pkt_duration_usec=10,
                          snr_stats=self.snr_stats, rate_stats=self.rate_stats)
        wireless_metric_2 = metrics.WirelessMetrics(**input_dict)
        self.assertEqual(self.wireless_metric, wireless_metric_2)
        self.assertNotEqual(self.wireless_metric, input_dict)

    def test_ne_works(self):
        wireless_metric_3 = metrics.WirelessMetrics(start_ts=0, end_ts=2, total_pkts=10, total_bytes=100,
                                               total_data_pkts=1, total_data_bytes=20, total_retx=1,
                                               total_trans_time_usec=100, avg_data_pkt_duration_usec=10,
                                               snr_stats=self.snr_stats, rate_stats=self.rate_stats)
        self.assertNotEqual(self.wireless_metric, wireless_metric_3)

    def test_update_stats_works(self):
        self.wireless_metric = metrics.WirelessMetrics()
        test_input = dict(start_ts=1, end_ts=2, total_pkts=10, total_bytes=100,
                                               total_data_pkts=1, total_data_bytes=20, total_retx=1,
                                               total_trans_time_usec=100, avg_data_pkt_duration_usec=10,
                                               snr_stats=self.snr_stats, rate_stats=self.rate_stats)
        self.wireless_metric.update_stats(**test_input)
        self.assertEqual(self.wireless_metric.total_pkts, 10)
        self.assertEqual(self.wireless_metric.total_bytes, 100)
        self.assertEqual(self.wireless_metric.total_data_pkts, 1)
        self.assertEqual(self.wireless_metric.total_data_bytes, 20)
        self.assertEqual(self.wireless_metric.total_retx, 1)
        self.assertEqual(self.wireless_metric.total_trans_time_usec, 100)
        self.assertEqual(self.wireless_metric.avg_data_pkt_duration_usec, 10)
        #rssi stats
        self.assertEqual(self.wireless_metric.snr_stats.min_val, -90)
        self.assertEqual(self.wireless_metric.snr_stats.max_val, -10)
        self.assertEqual(self.wireless_metric.snr_stats.num_samples, 10)
        #rssi stats
        self.assertEqual(self.wireless_metric.rate_stats.percentile_10, 2)
        self.assertEqual(self.wireless_metric.rate_stats.percentile_50, 24)
        self.assertEqual(self.wireless_metric.rate_stats.percentile_90, 48)
        self.assertEqual(self.wireless_metric.rate_stats.num_samples, 10)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWirelessMetrics)
    unittest.TextTestRunner(verbosity=2).run(suite)
