#!/usr/bin/env python3

import ipaddress
import unittest
import io
import json

import dobby.nwinfo.networksummary as networksummary
import dobby.nwmodel.endpoint as endpoint
import dobby.nwmodel.node as nodemodel
import dobby.nwmodel.flow as flow
import dobby.nwmodel.ipinfo as ipinfo
import dobby.nwmodel.phymodel as phymodel
import dobby.nwmetrics.metrics as metrics
import dobby.nwparser.parsemanager as parsemanager
import dobby.nwparser.parsenodesummary as nodesummaryparser
import dobby.utils.util as util

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestParseManager(unittest.TestCase):
    def setUp(self):
        self.addr1 = phymodel.PhysicalAddress(phy_address='C0:1A:DA:99:6B:76')
        self.addr2 = phymodel.PhysicalAddress(phy_address='33:33:00:00:00:16')
        self.addr3 = phymodel.PhysicalAddress(phy_address='98:FC:11:50:AF:A4')
        self.addr4 = phymodel.PhysicalAddress(phy_address='58:7F:57:EE:E0:9E')
        self.bssid = phymodel.PhysicalAddress(phy_address='98:FC:11:50:AF:A6')
        self.all_macs_sorted = sorted([str(self.addr1), str(self.addr2),
                                              str(self.addr3), str(self.addr4)])

        self.ip_1 = ipaddress.IPv4Address('192.168.1.113')
        self.ip_2 = ipaddress.IPv4Address('192.168.1.120')
        self.ip_3 = ipaddress.IPv4Address('54.148.159.16')

        self.wireless_json = {u'links': {u'link': [{u'@ap': u'C0:1A:DA:99:6B:76', u'@client': u'33:33:00:00:00:16', u'@bssid': u'98:FC:11:50:AF:A6', u'stream': {u'@total_data_bytes': u'496', u'@avg_noise': u'0', u'@total_data_pkts': u'4', u'@avg_data_pkt_size': u'124', u'@snr': u'-80/-80/-80', u'@rate': u'1/1/1', u'@total_retx': u'0', u'@avg_data_pkt_duration_usec': u'1808', u'@avg_signal': u'-80', u'@dir': u'AP-CLIENT', u'@total_pkts': u'4', u'@total_trans_time_usec': u'7232', u'@size': u'124/124/124'}}, {u'@ap': u'98:FC:11:50:AF:A4', u'@client': u'58:7F:57:EE:E0:9E', u'@bssid': u'98:FC:11:50:AF:A6', u'stream': [{u'@total_data_bytes': u'60', u'@avg_noise': u'0', u'@total_data_pkts': u'1', u'@avg_data_pkt_size': u'60', u'@snr': u'-80/-80/-80', u'@rate': u'24/24/24', u'@total_retx': u'1', u'@avg_data_pkt_duration_usec': u'198', u'@avg_signal': u'-80', u'@dir': u'AP-CLIENT', u'@total_pkts': u'1', u'@total_trans_time_usec': u'198', u'@size': u'60/60/60'}, {u'@total_data_bytes': u'10167', u'@avg_noise': u'0', u'@total_data_pkts': u'46', u'@avg_data_pkt_size': u'221', u'@snr': u'-68/-64/-61', u'@rate': u'11/11/18', u'@total_retx': u'13', u'@avg_data_pkt_duration_usec': u'661', u'@avg_signal': u'-65', u'@dir': u'CLIENT-AP', u'@total_pkts': u'46', u'@total_trans_time_usec': u'30418', u'@size': u'60/61/212'}]}]}}
        self.tcpmystery_json = {'trace': {'@file': '/tmp/dobby.pcap', 'flow': [{'@aggregate': '1', '@begin': '1486757294.498616999', '@dport': '5001', '@dst': '192.168.1.113', '@duration': '31.338471001', '@filepos': '56934', '@sport': '60194', '@src': '192.168.1.120', 'rtt': [{'@source': 'syn', '@value': '1.7e-05'}, {'@source': 'min', '@value': '1.7e-05'}, {'@source': 'avg', '@value': '0.00491831'}, {'@source': 'max', '@value': '0.995433'}], 'stream': [{'@beginseq': '2896214685', '@dir': '0', '@mtu': '1500', '@nack': '2', '@ndata': '15037', '@sentsackok': 'yes', '@seqlen': '21768626', 'semirtt': [{'@source': 'syn', '@value': '8e-06'}, {'@source': 'min', '@value': '8e-06'}, {'@n': '3464', '@source': 'avg', '@value': '0.00490331'}, {'@source': 'max', '@value': '0.995412'}, {'@n': '3464', '@source': 'var', '@value': '0.00170436'}]}, {'@beginseq': '723866139', '@dir': '1', '@mtu': '72', '@nack': '4614', '@ndata': '2', '@sentsackok': 'yes', '@seqlen': '2', 'semirtt': [{'@source': 'syn', '@value': '9e-06'}, {'@source': 'min', '@value': '9e-06'}, {'@n': '2', '@source': 'avg', '@value': '1.5e-05'}, {'@source': 'max', '@value': '2.1e-05'}, {'@n': '2', '@source': 'var', '@value': '7.2e-11'}]}]}, {'@aggregate': '2', '@begin': '1486757294.498906999', '@dport': '52124', '@dst': '192.168.1.120', '@duration': '114.929850001', '@filepos': '66228', '@sport': '22', '@src': '192.168.1.113', 'stream': [{'@beginseq': '3162875021', '@dir': '0', '@mtu': '168', '@nack': '0', '@ndata': '10', '@seqlen': '872', 'semirtt': [{'@source': 'syn', '@value': '0.000396'}, {'@source': 'min', '@value': '1.2e-05'}, {'@n': '5', '@source': 'avg', '@value': '0.0001546'}, {'@source': 'max', '@value': '0.000396'}, {'@n': '5', '@source': 'var', '@value': '2.50028e-08'}]}, {'@beginseq': '1439000513', '@dir': '1', '@mtu': '52', '@nack': '10', '@ndata': '0', '@seqlen': '0'}]}, {'@aggregate': '15', '@begin': '1486757401.300496999', '@dport': '443', '@dst': '54.148.159.16', '@duration': '0.414764001', '@filepos': '81432136', '@sport': '34018', '@src': '192.168.1.120', 'rtt': [{'@source': 'syn', '@value': '0.001358'}, {'@source': 'min', '@value': '0.000667'}, {'@source': 'avg', '@value': '0.0319902'}, {'@source': 'max', '@value': '0.214378'}], 'stream': [{'@beginseq': '2675085879', '@dir': '0', '@mtu': '323', '@nack': '15', '@ndata': '12', '@sentsackok': 'yes', '@seqlen': '674', 'semirtt': [{'@source': 'syn', '@value': '0.001264'}, {'@source': 'min', '@value': '0.000573'}, {'@n': '7', '@source': 'avg', '@value': '0.0317169'}, {'@source': 'max', '@value': '0.213781'}, {'@n': '7', '@source': 'var', '@value': '0.00644568'}]}, {'@beginseq': '3085039657', '@dir': '1', '@mtu': '1500', '@nack': '5', '@ndata': '10', '@sentsackok': 'yes', '@seqlen': '6359', 'semirtt': [{'@source': 'syn', '@value': '9.4e-05'}, {'@source': 'min', '@value': '9.4e-05'}, {'@n': '6', '@source': 'avg', '@value': '0.000273333'}, {'@source': 'max', '@value': '0.000597'}, {'@n': '6', '@source': 'var', '@value': '3.51571e-08'}]}]}]}}
        self.tcploss_json = {'trace': {'@file': '/tmp/dobby.pcap', 'flow': [{'@aggregate': '1', '@begin': '1486757294.498616999', '@dport': '5001', '@dst': '192.168.1.113', '@duration': '31.338471001', '@filepos': '56934', '@sport': '60194', '@src': '192.168.1.120', 'rtt': {'@source': 'minacklatency', '@value': '0.000017000'}, 'stream': [{'@beginseq': '2896214685', '@dir': '0', '@minacklatency': '0.000008000', '@nack': '2', '@ndata': '15037', '@nfloss': '21', '@nloss': '7707', '@sentsackok': 'yes', '@seqlen': '21768626', 'reordered': {'@n': '21'}, 'undelivered': {'@n': '7157'}}, {'@beginseq': '723866139', '@dir': '1', '@minacklatency': '0.000009000', '@nack': '4614', '@ndata': '2', '@nfloss': '0', '@nloss': '0', '@sentsackok': 'yes', '@seqlen': '2'}]}, {'@aggregate': '2', '@begin': '1486757294.498906999', '@dport': '52124', '@dst': '192.168.1.120', '@duration': '114.929850001', '@filepos': '66228', '@sport': '22', '@src': '192.168.1.113', 'stream': [{'@beginseq': '3162875021', '@dir': '0', '@minacklatency': '0.000011000', '@nack': '0', '@ndata': '10', '@nfloss': '2', '@nloss': '1', '@seqlen': '872', 'reordered': {'@n': '0'}, 'undelivered': {'@n': '2'}}, {'@beginseq': '1439000513', '@dir': '1', '@nack': '10', '@ndata': '0', '@nfloss': '0', '@nloss': '0', '@seqlen': '0'}]}, {'@aggregate': '15', '@begin': '1486757401.300496999', '@dport': '443', '@dst': '54.148.159.16', '@duration': '0.414764001', '@filepos': '81432136', '@sport': '34018', '@src': '192.168.1.120', 'rtt': {'@source': 'minacklatency', '@value': '0.000667000'}, 'stream': [{'@beginseq': '2675085879', '@dir': '0', '@minacklatency': '0.000573000', '@nack': '15', '@ndata': '12', '@nfloss': '0', '@nloss': '2', '@sentsackok': 'yes', '@seqlen': '674', 'reordered': {'@n': '0'}, 'undelivered': {'@n': '5'}}, {'@beginseq': '3085039657', '@dir': '1', '@minacklatency': '0.000094000', '@nack': '5', '@ndata': '10', '@nfloss': '1', '@nloss': '0', '@sentsackok': 'yes', '@seqlen': '6359', 'reordered': {'@n': '0'}, 'undelivered': {'@n': '0'}}]}]}}
        self.node_json = {'nodes': {'node': [{'@count': '42', '@count_eth_dst': '42', '@count_eth_src': '0', '@count_ip_dst': '30', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': 'FF:FF:FF:FF:FF:FF', 'ip': [{'@addr': '73.23.255.255', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '108.3.1.5', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '108.3.1.6', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '108.3.1.7', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '108.3.1.8', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '108.3.1.9', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}]}, {'@count': '50', '@count_eth_dst': '20', '@count_eth_src': '30', '@count_ip_dst': '20', '@count_ip_src': '30', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': 'B8:E8:56:1F:D6:FE', 'ip': [{'@addr': '36.48.72.96', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '5.45.26.173', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '6.45.26.173', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '7.45.26.173', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '8.45.26.173', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}]}, {'@count': '587', '@count_eth_dst': '373', '@count_eth_src': '214', '@count_ip_dst': '373', '@count_ip_src': '214', '@count_tcp_dst': '373', '@count_tcp_src': '206', '@ether': '98:FC:11:50:AF:A4', 'ip': [{'@addr': '52.54.141.132', '@hostname': '', 'port': {'@number': '47873', '@servicename': ''}}, {'@addr': '175.164.192.168', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '173.194.203.188', '@hostname': '', 'port': {'@number': '27668', '@servicename': ''}}, {'@addr': '216.58.195.78', '@hostname': '', 'port': {'@number': '47873', '@servicename': ''}}, {'@addr': '173.194.202.189', '@hostname': '', 'port': {'@number': '47873', '@servicename': ''}}, {'@addr': '216.58.194.206', '@hostname': '', 'port': {'@number': '47873', '@servicename': ''}}, {'@addr': '54.148.159.16', '@hostname': '', 'port': {'@number': '47873', '@servicename': ''}}, {'@addr': '172.217.6.46', '@hostname': '', 'port': {'@number': '47873', '@servicename': ''}}, {'@addr': '75.75.75.75', '@hostname': '', 'port': {'@number': '13568', '@servicename': ''}}, {'@addr': '216.58.192.4', '@hostname': '', 'port': {'@number': '47873', '@servicename': ''}}, {'@addr': '75.75.76.76', '@hostname': '', 'port': [{'@number': '5207', '@servicename': ''}, {'@number': '6743', '@servicename': ''}, {'@number': '6999', '@servicename': ''}, {'@number': '13568', '@servicename': ''}]}]}, {'@count': '110', '@count_eth_dst': '0', '@count_eth_src': '110', '@count_ip_dst': '0', '@count_ip_src': '110', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': '98:FC:11:50:AF:A6', 'ip': {'@addr': '8.130.132.139', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}, {'@count': '18', '@count_eth_dst': '18', '@count_eth_src': '0', '@count_ip_dst': '18', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': '5C:F6:DC:39:57:E5', 'ip': {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}, {'@count': '14', '@count_eth_dst': '14', '@count_eth_src': '0', '@count_ip_dst': '14', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': 'D0:E7:82:F1:90:90', 'ip': {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}, {'@count': '62548', '@count_eth_dst': '48409', '@count_eth_src': '14139', '@count_ip_dst': '48409', '@count_ip_src': '14139', '@count_tcp_dst': '48409', '@count_tcp_src': '14132', '@ether': 'C8:BC:C8:8D:38:F6', 'ip': [{'@addr': '192.168.1.113', '@hostname': '', 'port': [{'@number': '35091', '@servicename': ''}, {'@number': '5632', '@servicename': ''}]}, {'@addr': '56.246.192.168', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}]}, {'@count': '14', '@count_eth_dst': '14', '@count_eth_src': '0', '@count_ip_dst': '14', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': 'E4:F8:EF:BC:36:42', 'ip': {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}, {'@count': '63165', '@count_eth_dst': '14365', '@count_eth_src': '48800', '@count_ip_dst': '14365', '@count_ip_src': '48798', '@count_tcp_dst': '14338', '@count_tcp_src': '48786', '@ether': '74:DF:BF:66:7C:69', 'ip': [{'@addr': '1.1.0.0', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '227.25.27.255', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '1.113.116.223', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '192.168.1.120', '@hostname': '', 'port': [{'@number': '59668', '@servicename': ''}, {'@number': '58528', '@servicename': ''}, {'@number': '39606', '@servicename': ''}, {'@number': '22720', '@servicename': ''}]}, {'@addr': '1.113.0.0', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}]}, {'@count': '2', '@count_eth_dst': '2', '@count_eth_src': '0', '@count_ip_dst': '2', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': '33:33:00:00:00:FB', 'ip': {'@addr': '179.82.66.192', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}, {'@count': '4', '@count_eth_dst': '4', '@count_eth_src': '0', '@count_ip_dst': '4', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': '00:26:AB:17:A4:6A', 'ip': {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}, {'@count': '14', '@count_eth_dst': '14', '@count_eth_src': '0', '@count_ip_dst': '14', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': '34:E6:AD:BF:EC:53', 'ip': {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}, {'@count': '4', '@count_eth_dst': '4', '@count_eth_src': '0', '@count_ip_dst': '4', '@count_ip_src': '0', '@count_tcp_dst': '4', '@count_tcp_src': '0', '@ether': '01:00:5E:00:00:FB', 'ip': {'@addr': '224.0.0.251', '@hostname': '', 'port': {'@number': '59668', '@servicename': ''}}}, {'@count': '14', '@count_eth_dst': '14', '@count_eth_src': '0', '@count_ip_dst': '14', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': '44:33:4C:07:E9:DD', 'ip': {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}]}}
        self.ns = networksummary.NetworkSummary()
        self.ips = set()
        self.ethers = set()
        self.nodes = set()
        self.node_count = 0
        self.channel = 0
        #Node stuff
        for node in self.node_json['nodes']['node']:
            if node.get('@ether', None):
                self.ethers.add(node['@ether'].lower())
            if node.get('ip', None):
                if (type(node['ip']) == dict):
                    ips_to_process = [node['ip']]
                else:
                    ips_to_process = node['ip']
                assert(type(ips_to_process) == list)
                ip_list = [ip['@addr'] for ip in ips_to_process]
                self.ips.update(ip_list)
            self.node_count += 1
        #TCP Mystery
        self.tcp_info = set()
        self.tcp_keys = set()
        for flow in self.tcpmystery_json['trace']['flow']:
            self.ips.update([flow['@dst'], flow['@src']])
            self.tcp_info.add((flow['@src'], flow['@dst'], flow['@sport'], flow['@dport']))
            self.tcp_keys.add(str(flow['@src'] + "-" + flow['@sport'] + "-" + flow['@dst'] + "-" + flow['@dport']))

        #TCP loss
        for flow in self.tcploss_json['trace']['flow']:
            self.ips.update([flow['@dst'], flow['@src']])
            self.tcp_info.add((flow['@src'], flow['@dst'], flow['@sport'], flow['@dport']))
            self.tcp_keys.add(str(flow['@src'] + "-" + flow['@sport'] + "-" + flow['@dst'] + "-" + flow['@dport']))

        #Wireless Summary
        self.aps = set()
        self.clients = set()
        self.bssids = set()
        self.wifimodels = {}
        for link in self.wireless_json['links']['link']:
            self.aps.update([link['@ap']])
            self.clients.update([link['@client']])
            self.bssids.update([link['@bssid']])
            wifimodel = phymodel.WifiPhysicalModel(mac=phymodel.PhysicalAddress(link['@ap']))
            wifimodel.add_clients([link['@client']])
            self.wifimodels[link['@bssid']] = wifimodel
            self.ethers.update([link['@ap'].lower(), link['@client'].lower()])

        self.wireless_stream = io.StringIO(json.dumps(self.wireless_json))
        self.node_stream = io.StringIO(json.dumps(self.node_json))
        self.tcpmystery_stream = io.StringIO(json.dumps(self.tcpmystery_json))
        self.tcploss_stream = io.StringIO(json.dumps(self.tcploss_json))

        self.parse_manager = parsemanager.ParseManager()
        self.parse_manager.parse_summary(start_ts=1, end_ts=2,
                           wireless_stream=self.wireless_stream,
                           node_stream=self.node_stream,
                           tcploss_stream=self.tcploss_stream,
                           tcpmystery_stream=self.tcpmystery_stream)

    def tearDown(self):
        self.parse_manager = None

    def test_parse_summary(self):
        ns = self.parse_manager.summary_queue.pop()
        self.assertEqual(ns.start_ts, 1)
        self.assertEqual(ns.end_ts, 2)

        #Check ip to endpoints mapping
        self.assertEqual(len(ns.ip_to_endpoints), len(self.ips))
        self.assertListEqual(sorted(list(ns.ip_to_endpoints.keys())), sorted(self.ips))
        ips_from_endpoints = set()
        for endpoint in ns.ip_to_endpoints.values():
            ips_from_endpoints.update(list(endpoint.ip_infos.keys()))
        self.assertEqual(sorted(ips_from_endpoints),
                         sorted(self.ips))

        #Check mac to endpoints mapping
        self.assertEqual(len(ns.mac_to_endpoints), len(self.ethers))
        self.assertListEqual(sorted([x.lower() for x in ns.mac_to_endpoints.keys()]),
                             sorted(self.ethers))

        #Check cloud ips are correctly mapped
        cloud_ip_nodes = [node for node in ns.nodes.values() if node.node_type.value == nodemodel.NodeType.CLOUD_IP.value]
        self.assertEqual(len(cloud_ip_nodes), 11)

        #Check IP flows
        self.assertEqual(len(ns.ip_flows), len(self.tcp_info))
        self.assertEqual(len(ns.ip_flows), len(self.tcp_keys))
        self.assertEqual(sorted(ns.ip_flows.keys()), sorted(self.tcp_keys))
        node_endpoints = []
        for key, value in ns.nodes.items():
            node_endpoints.extend(value.endpoints)
        ips_from_node_endpoints = set()
        for endpoint in node_endpoints:
            ips_from_node_endpoints.update(list(endpoint.ip_infos.keys()))
        self.assertEqual(sorted(ips_from_node_endpoints),
                         sorted(self.ips))

        #Check wireless summary
        self.assertListEqual(sorted(ns.mac_to_endpoints.keys()), sorted(self.ethers))
        self.assertEqual(sorted([str(endpoint.phy_address) for endpoint in ns.mac_to_endpoints.values()]),
                         sorted(self.ethers))
        self.assertEqual(sorted(ns.phy_models.keys()), sorted([(str(self.bssid), self.channel)]))
        self.assertEqual(sorted(ns.edges.keys()),
                         sorted([(str(self.addr1), str(self.addr2)), (str(self.addr3), str(self.addr4))]))

    def test_find_summary_works(self):
        ns1 = self.parse_manager.find_summary(1)
        ns2 = self.parse_manager.find_summary(1.5)
        ns3 = self.parse_manager.find_summary(2)
        self.assertEqual(ns1.start_ts, 1)
        self.assertEqual(ns1.end_ts, 2)
        self.assertEqual(ns2.start_ts, 1)
        self.assertEqual(ns2.end_ts, 2)
        self.assertIsNone(ns3)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParseManager)
    unittest.TextTestRunner(verbosity=2).run(suite)
