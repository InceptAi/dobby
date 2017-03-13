#!/usr/bin/env python3

import ipaddress
import unittest

import dobby.nwinfo.networksummary as networksummary
import dobby.nwmodel.endpoint as endpoint
import dobby.nwmodel.edge as edge
import dobby.nwmodel.node as node
import dobby.nwmodel.flow as flow
import dobby.nwmodel.ipinfo as ipinfo
import dobby.nwmetrics.metrics as metrics
import dobby.nwparser.parsetcploss as tcplossparser
import dobby.utils.util as util
__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestParseTCPLossSummary(unittest.TestCase):
    def setUp(self):
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
        self.ns = networksummary.NetworkSummary()
        self.tcploss_parser = tcplossparser.ParseTCPLossSummary()

    def tearDown(self):
        self.tcploss_json = None

    def test_validate_parsing(self):
        self.tcploss_parser.parse_summary(tcploss_json=self.tcploss_json, network_summary=self.ns)
        self.assertEqual(len(self.ns.ip_to_endpoints), len(self.ips))
        self.assertEqual(len(self.ns.ip_flows), len(self.tcp_info))
        self.assertEqual(len(self.ns.nodes), len(self.ips))
        self.assertListEqual(sorted(self.ns.ip_to_endpoints.keys()), sorted(self.ips))

        ips_to_compare = set()
        for endpoint in self.ns.ip_to_endpoints.values():
            ips_to_compare.update(list(endpoint.ip_infos.keys()))
        self.assertEqual(sorted(ips_to_compare), sorted(self.ips))

        ips_to_compare = set()
        for endpoint in self.ns.ip_to_endpoints.values():
            ips_to_compare.update([str(ip_info.ipv4address) for ip_info in endpoint.ip_infos.values()])
        self.assertEqual(sorted(ips_to_compare), sorted(self.ips))

        self.assertEqual(sorted(self.ns.ip_flows.keys()), sorted(self.tcp_keys))

        node_endpoints = []
        ips_to_compare = set()
        for key, value in self.ns.nodes.items():
            node_endpoints.extend(value.endpoints)
        for endpoint in node_endpoints:
            ips_to_compare.update([str(ip_info.ipv4address) for ip_info in endpoint.ip_infos.values()])
        self.assertEqual(sorted(ips_to_compare), sorted(self.ips))

    def test_validate_metrics(self):
        self.tcploss_parser.parse_summary(tcploss_json=self.tcploss_json, network_summary=self.ns)
        metric1 = {'total_loss': 7728}
        metric1_src_to_dst = {'total_loss': 7728}
        metric1_dst_to_src = {'total_loss': 0}
        flow1 = self.ns.ip_flows["192.168.1.120-60194-192.168.1.113-5001"]
        self.assertIsNotNone(flow1)
        self.assertTrue(isinstance(flow1, flow.TCPFlow))
        self.assertEqual(flow1.flow_type.value, flow.FlowType.TCP.value)
        self.assertDictEqual(flow1.flow_metrics.__dict__, metrics.TCPMetrics(**metric1).__dict__)
        self.assertTrue(isinstance(flow1.flow_metrics, metrics.TCPMetrics))
        self.assertEqual(flow1.flow_metrics, metrics.TCPMetrics(**metric1))
        self.assertEqual(flow1.flow_metrics_src_to_dst, metrics.TCPMetrics(**metric1_src_to_dst))
        self.assertEqual(flow1.flow_metrics_dst_to_src, metrics.TCPMetrics(**metric1_dst_to_src))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParseTCPLossSummary)
    unittest.TextTestRunner(verbosity=2).run(suite)
