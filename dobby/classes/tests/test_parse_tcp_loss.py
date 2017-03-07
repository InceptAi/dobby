#!/usr/bin/env python3

from dobby.classes.endpoint import *
from dobby.classes.phymodel import *
from dobby.classes.node import *
from dobby.classes.ipinfo import *
from dobby.classes.node import *
from dobby.classes.flow import *
from dobby.classes.edge import *
from dobby.classes.parse import *
from dobby.classes.metrics import *
import ipaddress
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestParseTCPLossSummary(unittest.TestCase):
    def setUp(self):
        IP_TO_ENDPOINTS = {}
        NODES = {}
        IP_FLOWS = {}
        self.ip_1 = ipaddress.IPv4Address('192.168.1.113')
        self.ip_2 = ipaddress.IPv4Address('192.168.1.120')
        self.ip_3 = ipaddress.IPv4Address('54.148.159.16')
        self.tcploss_json = {'trace': {'@file': '/tmp/dobby.pcap', 'flow': [{'@aggregate': '1', '@begin': '1486757294.498616999', '@dport': '5001', '@dst': '192.168.1.113', '@duration': '31.338471001', '@filepos': '56934', '@sport': '60194', '@src': '192.168.1.120', 'rtt': {'@source': 'minacklatency', '@value': '0.000017000'}, 'stream': [{'@beginseq': '2896214685', '@dir': '0', '@minacklatency': '0.000008000', '@nack': '2', '@ndata': '15037', '@nfloss': '21', '@nloss': '7707', '@sentsackok': 'yes', '@seqlen': '21768626', 'reordered': {'@n': '21'}, 'undelivered': {'@n': '7157'}}, {'@beginseq': '723866139', '@dir': '1', '@minacklatency': '0.000009000', '@nack': '4614', '@ndata': '2', '@nfloss': '0', '@nloss': '0', '@sentsackok': 'yes', '@seqlen': '2'}]}, {'@aggregate': '2', '@begin': '1486757294.498906999', '@dport': '52124', '@dst': '192.168.1.120', '@duration': '114.929850001', '@filepos': '66228', '@sport': '22', '@src': '192.168.1.113', 'stream': [{'@beginseq': '3162875021', '@dir': '0', '@minacklatency': '0.000011000', '@nack': '0', '@ndata': '10', '@nfloss': '2', '@nloss': '1', '@seqlen': '872', 'reordered': {'@n': '0'}, 'undelivered': {'@n': '2'}}, {'@beginseq': '1439000513', '@dir': '1', '@nack': '10', '@ndata': '0', '@nfloss': '0', '@nloss': '0', '@seqlen': '0'}]}, {'@aggregate': '15', '@begin': '1486757401.300496999', '@dport': '443', '@dst': '54.148.159.16', '@duration': '0.414764001', '@filepos': '81432136', '@sport': '34018', '@src': '192.168.1.120', 'rtt': {'@source': 'minacklatency', '@value': '0.000667000'}, 'stream': [{'@beginseq': '2675085879', '@dir': '0', '@minacklatency': '0.000573000', '@nack': '15', '@ndata': '12', '@nfloss': '0', '@nloss': '2', '@sentsackok': 'yes', '@seqlen': '674', 'reordered': {'@n': '0'}, 'undelivered': {'@n': '5'}}, {'@beginseq': '3085039657', '@dir': '1', '@minacklatency': '0.000094000', '@nack': '5', '@ndata': '10', '@nfloss': '1', '@nloss': '0', '@sentsackok': 'yes', '@seqlen': '6359', 'reordered': {'@n': '0'}, 'undelivered': {'@n': '0'}}]}]}}
        self.ips = set()
        self.tcp_info = []
        self.tcp_keys = []
        for flow in self.tcploss_json['trace']['flow']:
            self.ips.update([flow['@dst'], flow['@src']])
            self.tcp_info.append((flow['@src'], flow['@dst'], flow['@sport'], flow['@dport']))
            self.tcp_keys.append(str(flow['@src'] + "-" + flow['@sport'] + "-" + flow['@dst'] + "-" + flow['@dport']))
        self.tcploss = ParseTCPLossSummary(tcploss_json=self.tcploss_json)

    def tearDown(self):
        self.tcploss_json = None

    def test_validate_parsing(self):
        self.tcploss.parse_summary()
        self.assertEqual(len(IP_TO_ENDPOINTS), len(self.ips))
        self.assertEqual(len(IP_FLOWS), len(self.tcp_info))
        self.assertEqual(len(NODES), len(self.ips))
        self.assertListEqual(sorted(IP_TO_ENDPOINTS.keys()), sorted(self.ips))
        self.assertEqual(sorted([str(endpoint.ip_info.ipv4address) for endpoint in IP_TO_ENDPOINTS.values()]),
                         sorted(self.ips))
        self.assertEqual(sorted(IP_FLOWS.keys()), sorted(self.tcp_keys))
        node_endpoints = []
        for key, value in NODES.items():
            node_endpoints.extend(value.endpoints)
        self.assertEqual(sorted([str(x.ip_info.ipv4address) for x in node_endpoints]),
                         sorted(self.ips))

    def test_validate_metrics(self):
        self.tcploss.parse_summary()
        metric1 = {'total_loss': 7728}
        metric1_src_to_dst = {'total_loss': 7728}
        metric1_dst_to_src = {'total_loss': 0}
        flow1 = IP_FLOWS["192.168.1.120-60194-192.168.1.113-5001"]
        self.assertIsNotNone(flow1)
        self.assertTrue(isinstance(flow1, TCPFlow))
        self.assertEqual(flow1.flow_type.value, FlowType.TCP.value)
        self.assertDictEqual(flow1.flow_metrics.__dict__, TCPMetrics(**metric1).__dict__)
        self.assertTrue(isinstance(flow1.flow_metrics, TCPMetrics))
        self.assertEqual(flow1.flow_metrics, TCPMetrics(**metric1))
        self.assertEqual(flow1.flow_metrics_src_to_dst, TCPMetrics(**metric1_src_to_dst))
        self.assertEqual(flow1.flow_metrics_dst_to_src, TCPMetrics(**metric1_dst_to_src))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParseTCPLossSummary)
    unittest.TextTestRunner(verbosity=2).run(suite)
