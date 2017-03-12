#!/usr/bin/env python3
import ipaddress
import unittest

import dobby.nwinfo.networksummary as networksummary
import dobby.nwmodel.edge as edge
import dobby.nwmodel.endpoint as endpoint
import dobby.nwmodel.flow as flow
import dobby.nwmodel.ipinfo as ipinfo
import dobby.nwmetrics.metrics as metrics
import dobby.nwmodel.node as node
import dobby.nwparser.parsetcpmystery as tcpmysteryparser
import dobby.utils.util as util

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestParseTCPMysterySummary(unittest.TestCase):
    def setUp(self):
        self.ip_1 = ipaddress.IPv4Address('192.168.1.113')
        self.ip_2 = ipaddress.IPv4Address('192.168.1.120')
        self.ip_3 = ipaddress.IPv4Address('54.148.159.16')
        self.tcpmystery_json = {'trace': {'@file': '/tmp/dobby.pcap', 'flow': [{'@aggregate': '1', '@begin': '1486757294.498616999', '@dport': '5001', '@dst': '192.168.1.113', '@duration': '31.338471001', '@filepos': '56934', '@sport': '60194', '@src': '192.168.1.120', 'rtt': [{'@source': 'syn', '@value': '1.7e-05'}, {'@source': 'min', '@value': '1.7e-05'}, {'@source': 'avg', '@value': '0.00491831'}, {'@source': 'max', '@value': '0.995433'}], 'stream': [{'@beginseq': '2896214685', '@dir': '0', '@mtu': '1500', '@nack': '2', '@ndata': '15037', '@sentsackok': 'yes', '@seqlen': '21768626', 'semirtt': [{'@source': 'syn', '@value': '8e-06'}, {'@source': 'min', '@value': '8e-06'}, {'@n': '3464', '@source': 'avg', '@value': '0.00490331'}, {'@source': 'max', '@value': '0.995412'}, {'@n': '3464', '@source': 'var', '@value': '0.00170436'}]}, {'@beginseq': '723866139', '@dir': '1', '@mtu': '72', '@nack': '4614', '@ndata': '2', '@sentsackok': 'yes', '@seqlen': '2', 'semirtt': [{'@source': 'syn', '@value': '9e-06'}, {'@source': 'min', '@value': '9e-06'}, {'@n': '2', '@source': 'avg', '@value': '1.5e-05'}, {'@source': 'max', '@value': '2.1e-05'}, {'@n': '2', '@source': 'var', '@value': '7.2e-11'}]}]}, {'@aggregate': '2', '@begin': '1486757294.498906999', '@dport': '52124', '@dst': '192.168.1.120', '@duration': '114.929850001', '@filepos': '66228', '@sport': '22', '@src': '192.168.1.113', 'stream': [{'@beginseq': '3162875021', '@dir': '0', '@mtu': '168', '@nack': '0', '@ndata': '10', '@seqlen': '872', 'semirtt': [{'@source': 'syn', '@value': '0.000396'}, {'@source': 'min', '@value': '1.2e-05'}, {'@n': '5', '@source': 'avg', '@value': '0.0001546'}, {'@source': 'max', '@value': '0.000396'}, {'@n': '5', '@source': 'var', '@value': '2.50028e-08'}]}, {'@beginseq': '1439000513', '@dir': '1', '@mtu': '52', '@nack': '10', '@ndata': '0', '@seqlen': '0'}]}, {'@aggregate': '15', '@begin': '1486757401.300496999', '@dport': '443', '@dst': '54.148.159.16', '@duration': '0.414764001', '@filepos': '81432136', '@sport': '34018', '@src': '192.168.1.120', 'rtt': [{'@source': 'syn', '@value': '0.001358'}, {'@source': 'min', '@value': '0.000667'}, {'@source': 'avg', '@value': '0.0319902'}, {'@source': 'max', '@value': '0.214378'}], 'stream': [{'@beginseq': '2675085879', '@dir': '0', '@mtu': '323', '@nack': '15', '@ndata': '12', '@sentsackok': 'yes', '@seqlen': '674', 'semirtt': [{'@source': 'syn', '@value': '0.001264'}, {'@source': 'min', '@value': '0.000573'}, {'@n': '7', '@source': 'avg', '@value': '0.0317169'}, {'@source': 'max', '@value': '0.213781'}, {'@n': '7', '@source': 'var', '@value': '0.00644568'}]}, {'@beginseq': '3085039657', '@dir': '1', '@mtu': '1500', '@nack': '5', '@ndata': '10', '@sentsackok': 'yes', '@seqlen': '6359', 'semirtt': [{'@source': 'syn', '@value': '9.4e-05'}, {'@source': 'min', '@value': '9.4e-05'}, {'@n': '6', '@source': 'avg', '@value': '0.000273333'}, {'@source': 'max', '@value': '0.000597'}, {'@n': '6', '@source': 'var', '@value': '3.51571e-08'}]}]}]}}
        self.ips = set()
        self.tcp_info = []
        self.tcp_keys = []
        for flow in self.tcpmystery_json['trace']['flow']:
            self.ips.update([flow['@dst'], flow['@src']])
            self.tcp_info.append((flow['@src'], flow['@dst'], flow['@sport'], flow['@dport']))
            self.tcp_keys.append(str(flow['@src'] + "-" + flow['@sport'] + "-" + flow['@dst'] + "-" + flow['@dport']))
        self.ns = networksummary.NetworkSummary()
        self.tcpmystery_parser = tcpmysteryparser.ParseTCPMysterySummary()

    def tearDown(self):
        self.tcpmystery_json = None

    def test_validate_parsing(self):
        self.tcpmystery_parser.parse_summary(tcpmystery_json=self.tcpmystery_json, network_summary=self.ns)
        self.assertEqual(len(self.ns.ip_to_endpoints), len(self.ips))
        self.assertEqual(len(self.ns.ip_flows), len(self.tcp_info))
        self.assertEqual(len(self.ns.nodes), len(self.ips))
        self.assertListEqual(sorted(self.ns.ip_to_endpoints.keys()), sorted(self.ips))
        self.assertEqual(sorted([str(endpoint.ip_info.ipv4address) for endpoint in self.ns.ip_to_endpoints.values()]),
                         sorted(self.ips))
        self.assertEqual(sorted(self.ns.ip_flows.keys()), sorted(self.tcp_keys))
        node_endpoints = []
        for key, value in self.ns.nodes.items():
            node_endpoints.extend(value.endpoints)
        self.assertEqual(sorted([str(x.ip_info.ipv4address) for x in node_endpoints]),
                         sorted(self.ips))

    def test_validate_metrics(self):
        self.tcpmystery_parser.parse_summary(tcpmystery_json=self.tcpmystery_json, network_summary=self.ns)
        duration1 = 31.338471001
        start1 = 1486757294.498616999
        rtt1 = {'min_val': 1.7e-05, 'max_val': 0.995433, 'avg_val': 0.00491831}
        metric1 = {'start_ts': start1,
                   'end_ts': start1 + duration1,
                   'duration': duration1,
                   'rtt_stats': metrics.Stats(**rtt1)}
        rtt1_src_to_dst = {'min_val': 8e-06, 'max_val': 0.995412, 'avg_val': 0.00490331, 'var_val': 0.00170436}
        metric1_src_to_dst = {'start_ts': start1,
                              'end_ts': start1 + duration1,
                              'total_pkts': 15037.0,
                              'total_bytes': 21768626.0,
                              'mtu': 1500.0,
                              'total_acks': 2.0,
                              'rtt_stats':metrics.Stats(**rtt1_src_to_dst)}

        rtt1_dst_to_src = {'min_val': 9e-06, 'max_val': 2.1e-05, 'avg_val': 1.5e-05, 'var_val': 7.2e-11}
        metric1_dst_to_src = {'start_ts': start1,
                              'end_ts': start1 + duration1,
                              'total_pkts': 2.0,
                              'total_bytes': 2.0,
                              'mtu': 72.0,
                              'total_acks': 4614.0,
                              'rtt_stats': metrics.Stats(**rtt1_dst_to_src)}
        flow1 = self.ns.ip_flows["192.168.1.120-60194-192.168.1.113-5001"]
        self.assertIsNotNone(flow1)
        self.assertTrue(isinstance(flow1, flow.TCPFlow))
        self.assertEqual(flow1.flow_type.value, flow.FlowType.TCP.value)
        self.assertEqual(flow1.flow_metrics.rtt_stats.__dict__, metrics.TCPMetrics(**metric1).rtt_stats.__dict__)
        self.assertDictEqual(flow1.flow_metrics.__dict__, metrics.TCPMetrics(**metric1).__dict__)
        self.assertTrue(isinstance(flow1.flow_metrics, metrics.TCPMetrics))
        self.assertEqual(flow1.flow_metrics, metrics.TCPMetrics(**metric1))
        self.assertEqual(flow1.flow_metrics_src_to_dst, metrics.TCPMetrics(**metric1_src_to_dst))
        self.assertEqual(flow1.flow_metrics_dst_to_src, metrics.TCPMetrics(**metric1_dst_to_src))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParseTCPMysterySummary)
    unittest.TextTestRunner(verbosity=2).run(suite)
