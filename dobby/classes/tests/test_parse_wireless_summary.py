#!/usr/bin/env python3

from dobby.classes.endpoint import *
from dobby.classes.phymodel import *
from dobby.classes.node import *
from dobby.classes.ipinfo import *
from dobby.classes.node import *
from dobby.classes.flow import *
from dobby.classes.edge import *
from dobby.classes.parse import *
#import dobby.classes.parse as parse
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestParseWirelessSummary(unittest.TestCase):
    def setUp(self):
        MAC_TO_ENDPOINTS = {}
        NODES = {}
        EDGES = {}
        PHYMODELS = {}
        self.channel = 0
        self.addr1 = PhysicalAddress(phy_address='C0:1A:DA:99:6B:76')
        self.addr2 = PhysicalAddress(phy_address='33:33:00:00:00:16')
        self.addr3 = PhysicalAddress(phy_address='98:FC:11:50:AF:A4')
        self.addr4 = PhysicalAddress(phy_address='58:7F:57:EE:E0:9E')
        self.bssid = PhysicalAddress(phy_address='98:FC:11:50:AF:A6')
        self.all_macs_sorted = sorted([str(self.addr1), str(self.addr2),
                                      str(self.addr3), str(self.addr4)])
        self.wireless_json = {u'links': {u'link': [{u'@ap': u'C0:1A:DA:99:6B:76', u'@client': u'33:33:00:00:00:16', u'@bssid': u'98:FC:11:50:AF:A6', u'stream': {u'@total_data_bytes': u'496', u'@avg_noise': u'0', u'@total_data_pkts': u'4', u'@avg_data_pkt_size': u'124', u'@snr': u'-80/-80/-80', u'@rate': u'1/1/1', u'@total_retx': u'0', u'@avg_data_pkt_duration_usec': u'1808', u'@avg_signal': u'-80', u'@dir': u'AP-CLIENT', u'@total_pkts': u'4', u'@total_trans_time_usec': u'7232', u'@size': u'124/124/124'}}, {u'@ap': u'98:FC:11:50:AF:A4', u'@client': u'58:7F:57:EE:E0:9E', u'@bssid': u'98:FC:11:50:AF:A6', u'stream': [{u'@total_data_bytes': u'60', u'@avg_noise': u'0', u'@total_data_pkts': u'1', u'@avg_data_pkt_size': u'60', u'@snr': u'-80/-80/-80', u'@rate': u'24/24/24', u'@total_retx': u'1', u'@avg_data_pkt_duration_usec': u'198', u'@avg_signal': u'-80', u'@dir': u'AP-CLIENT', u'@total_pkts': u'1', u'@total_trans_time_usec': u'198', u'@size': u'60/60/60'}, {u'@total_data_bytes': u'10167', u'@avg_noise': u'0', u'@total_data_pkts': u'46', u'@avg_data_pkt_size': u'221', u'@snr': u'-68/-64/-61', u'@rate': u'11/11/18', u'@total_retx': u'13', u'@avg_data_pkt_duration_usec': u'661', u'@avg_signal': u'-65', u'@dir': u'CLIENT-AP', u'@total_pkts': u'46', u'@total_trans_time_usec': u'30418', u'@size': u'60/61/212'}]}]}}
        self.wireless = ParseWirelessSummary(wireless_json=self.wireless_json)

    def tearDown(self):
        self.wireless_json = None

    def test_validate_parsing(self):
        self.wireless.parse_summary()
        self.assertEqual(len(MAC_TO_ENDPOINTS), 4)
        self.assertEqual(len(PHYMODELS), 1)
        self.assertEqual(len(EDGES), 2)
        self.assertEqual(len(NODES), 4)
        #self.assertListEqual(sorted([str(mac) for mac in MAC_TO_ENDPOINTS.keys()]), self.all_macs_sorted)
        self.assertListEqual(sorted(MAC_TO_ENDPOINTS.keys()), self.all_macs_sorted)
        self.assertEqual(sorted([str(endpoint.phy_address) for endpoint in MAC_TO_ENDPOINTS.values()]),
                         self.all_macs_sorted)
        self.assertEqual(sorted(PHYMODELS.keys()), sorted([(str(self.bssid), self.channel)]))
        self.assertEqual(sorted(EDGES.keys()),
                         sorted([(str(self.addr1), str(self.addr2)), (str(self.addr3), str(self.addr4))]))
        node_endpoints = []
        for key, value in NODES.items():
            node_endpoints.extend(value.endpoints)
        self.assertEqual(sorted([str(x.phy_address) for x in node_endpoints]),
                         self.all_macs_sorted)

    def test_validate_metrics(self):
        self.wireless.parse_summary()
        edge1 = EDGES[(str(self.addr1), str(self.addr2))]
        edge2 = EDGES[(str(self.addr3), str(self.addr4))]
        self.assertIsNotNone(edge1)
        self.assertIsNotNone(edge2)
        snr_stats1 = Stats(percentile_10=-80.0, percentile_50=-80.0, percentile_90=-80.0, num_samples=4.0)
        rate_stats1 = Stats(percentile_10=1.0, percentile_50=1.0, percentile_90=1.0, num_samples=4.0)
        size_stats1 = Stats(percentile_10=124.0, percentile_50=124.0, percentile_90=124.0, num_samples=4.0)
        metrics1_ab = WirelessMetrics(total_pkts=4.0, total_data_pkts=4.0, total_data_bytes=496.0,
                                        total_retx=0.0, total_trans_time_usec=7232.0,
                                        avg_data_pkt_duration_usec=1808.0,
                                        snr_stats=snr_stats1, rate_stats=rate_stats1,
                                        size_stats=size_stats1)
        self.assertIsNone(edge1.edge_metrics)
        self.assertIsNotNone(edge1.edge_metrics_ab)
        self.assertIsNone(edge1.edge_metrics_ba)
        self.assertEqual(metrics1_ab, edge1.edge_metrics_ab)

    def test_incorrect_stats_string_returns_none(self):
        #Modifying the first snr string from -80/-80/-80 to -80/-80
        self.wireless_json = {u'links': {u'link': [{u'@ap': u'C0:1A:DA:99:6B:76', u'@client': u'33:33:00:00:00:16', u'@bssid': u'98:FC:11:50:AF:A6', u'stream': {u'@total_data_bytes': u'496', u'@avg_noise': u'0', u'@total_data_pkts': u'4', u'@avg_data_pkt_size': u'124', u'@snr': u'-80/-80', u'@rate': u'1/1/1', u'@total_retx': u'0', u'@avg_data_pkt_duration_usec': u'1808', u'@avg_signal': u'-80', u'@dir': u'AP-CLIENT', u'@total_pkts': u'4', u'@total_trans_time_usec': u'7232', u'@size': u'124/124/124'}}, {u'@ap': u'98:FC:11:50:AF:A4', u'@client': u'58:7F:57:EE:E0:9E', u'@bssid': u'98:FC:11:50:AF:A6', u'stream': [{u'@total_data_bytes': u'60', u'@avg_noise': u'0', u'@total_data_pkts': u'1', u'@avg_data_pkt_size': u'60', u'@snr': u'-80/-80/-80', u'@rate': u'24/24/24', u'@total_retx': u'1', u'@avg_data_pkt_duration_usec': u'198', u'@avg_signal': u'-80', u'@dir': u'AP-CLIENT', u'@total_pkts': u'1', u'@total_trans_time_usec': u'198', u'@size': u'60/60/60'}, {u'@total_data_bytes': u'10167', u'@avg_noise': u'0', u'@total_data_pkts': u'46', u'@avg_data_pkt_size': u'221', u'@snr': u'-68/-64/-61', u'@rate': u'11/11/18', u'@total_retx': u'13', u'@avg_data_pkt_duration_usec': u'661', u'@avg_signal': u'-65', u'@dir': u'CLIENT-AP', u'@total_pkts': u'46', u'@total_trans_time_usec': u'30418', u'@size': u'60/61/212'}]}]}}
        self.wireless = ParseWirelessSummary(wireless_json=self.wireless_json)
        self.wireless.parse_summary()
        edge1 = EDGES[(str(self.addr1), str(self.addr2))]
        self.assertIsNone(edge1.edge_metrics_ab.snr_stats)

    def test_non_integer_stats_string_returns_none(self):
        #Modifying the first snr string from -80/-80/-80 to foo/-80/-80
        self.wireless_json = {u'links': {u'link': [{u'@ap': u'C0:1A:DA:99:6B:76', u'@client': u'33:33:00:00:00:16', u'@bssid': u'98:FC:11:50:AF:A6', u'stream': {u'@total_data_bytes': u'496', u'@avg_noise': u'0', u'@total_data_pkts': u'4', u'@avg_data_pkt_size': u'124', u'@snr': u'foo/-80/-80', u'@rate': u'1/1/1', u'@total_retx': u'0', u'@avg_data_pkt_duration_usec': u'1808', u'@avg_signal': u'-80', u'@dir': u'AP-CLIENT', u'@total_pkts': u'4', u'@total_trans_time_usec': u'7232', u'@size': u'124/124/124'}}, {u'@ap': u'98:FC:11:50:AF:A4', u'@client': u'58:7F:57:EE:E0:9E', u'@bssid': u'98:FC:11:50:AF:A6', u'stream': [{u'@total_data_bytes': u'60', u'@avg_noise': u'0', u'@total_data_pkts': u'1', u'@avg_data_pkt_size': u'60', u'@snr': u'-80/-80/-80', u'@rate': u'24/24/24', u'@total_retx': u'1', u'@avg_data_pkt_duration_usec': u'198', u'@avg_signal': u'-80', u'@dir': u'AP-CLIENT', u'@total_pkts': u'1', u'@total_trans_time_usec': u'198', u'@size': u'60/60/60'}, {u'@total_data_bytes': u'10167', u'@avg_noise': u'0', u'@total_data_pkts': u'46', u'@avg_data_pkt_size': u'221', u'@snr': u'-68/-64/-61', u'@rate': u'11/11/18', u'@total_retx': u'13', u'@avg_data_pkt_duration_usec': u'661', u'@avg_signal': u'-65', u'@dir': u'CLIENT-AP', u'@total_pkts': u'46', u'@total_trans_time_usec': u'30418', u'@size': u'60/61/212'}]}]}}
        self.wireless = ParseWirelessSummary(wireless_json=self.wireless_json)
        self.wireless.parse_summary()
        edge1 = EDGES[(str(self.addr1), str(self.addr2))]
        self.assertIsNone(edge1.edge_metrics_ab.snr_stats)

    def test_non_integer_total_data_bytes_returns_none(self):
        #Modifying the first total pkts from 496 to foo
        self.wireless_json = {u'links': {u'link': [{u'@ap': u'C0:1A:DA:99:6B:76', u'@client': u'33:33:00:00:00:16', u'@bssid': u'98:FC:11:50:AF:A6', u'stream': {u'@total_data_bytes': u'foo', u'@avg_noise': u'0', u'@total_data_pkts': u'4', u'@avg_data_pkt_size': u'124', u'@snr': u'-80/-80/-80', u'@rate': u'1/1/1', u'@total_retx': u'0', u'@avg_data_pkt_duration_usec': u'1808', u'@avg_signal': u'-80', u'@dir': u'AP-CLIENT', u'@total_pkts': u'4', u'@total_trans_time_usec': u'7232', u'@size': u'124/124/124'}}, {u'@ap': u'98:FC:11:50:AF:A4', u'@client': u'58:7F:57:EE:E0:9E', u'@bssid': u'98:FC:11:50:AF:A6', u'stream': [{u'@total_data_bytes': u'60', u'@avg_noise': u'0', u'@total_data_pkts': u'1', u'@avg_data_pkt_size': u'60', u'@snr': u'-80/-80/-80', u'@rate': u'24/24/24', u'@total_retx': u'1', u'@avg_data_pkt_duration_usec': u'198', u'@avg_signal': u'-80', u'@dir': u'AP-CLIENT', u'@total_pkts': u'1', u'@total_trans_time_usec': u'198', u'@size': u'60/60/60'}, {u'@total_data_bytes': u'10167', u'@avg_noise': u'0', u'@total_data_pkts': u'46', u'@avg_data_pkt_size': u'221', u'@snr': u'-68/-64/-61', u'@rate': u'11/11/18', u'@total_retx': u'13', u'@avg_data_pkt_duration_usec': u'661', u'@avg_signal': u'-65', u'@dir': u'CLIENT-AP', u'@total_pkts': u'46', u'@total_trans_time_usec': u'30418', u'@size': u'60/61/212'}]}]}}
        self.wireless = ParseWirelessSummary(wireless_json=self.wireless_json)
        self.wireless.parse_summary()
        edge1 = EDGES[(str(self.addr1), str(self.addr2))]
        self.assertIsNone(edge1.edge_metrics_ab.total_data_bytes)

#    def test_validate_properties(self):

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParseWirelessSummary)
    unittest.TextTestRunner(verbosity=2).run(suite)
