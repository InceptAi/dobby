#!/usr/bin/env python3

from dobby.classes.endpoint import *
from dobby.classes.phymodel import *
from dobby.classes.node import *
from dobby.classes.ipinfo import *
from dobby.classes.node import *
from dobby.classes.flow import *
from dobby.classes.edge import *
#from dobby.classes.parse import *
from dobby.classes.metrics import *
#from dobby.classes.parse import MAC_TO_ENDPOINTS, NODES
import dobby.classes.parse as parse
import ipaddress
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestParseNodeSummary(unittest.TestCase):
    def setUp(self):
        print ("Coming to setup")
        print ("Len:IP_TO_ENDPOINTS", len(parse.IP_TO_ENDPOINTS))
        print ("Len:MAC_TO_ENDPOINTS", len(parse.MAC_TO_ENDPOINTS))
        print ("Len:NODES", len(parse.NODES))
        parse.IP_TO_ENDPOINTS = {}
        parse.MAC_TO_ENDPOINTS = {}
        parse.NODES = {}
        self.ip_1 = ipaddress.IPv4Address('192.168.1.113')
        self.ip_2 = ipaddress.IPv4Address('192.168.1.120')
        self.ip_3 = ipaddress.IPv4Address('54.148.159.16')
        self.node_json = {'nodes': {'node': [{'@count': '42', '@count_eth_dst': '42', '@count_eth_src': '0', '@count_ip_dst': '30', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': 'FF:FF:FF:FF:FF:FF', 'ip': [{'@addr': '73.23.255.255', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '108.3.1.5', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '108.3.1.6', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '108.3.1.7', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '108.3.1.8', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '108.3.1.9', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}]}, {'@count': '50', '@count_eth_dst': '20', '@count_eth_src': '30', '@count_ip_dst': '20', '@count_ip_src': '30', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': 'B8:E8:56:1F:D6:FE', 'ip': [{'@addr': '36.48.72.96', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '5.45.26.173', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '6.45.26.173', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '7.45.26.173', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '8.45.26.173', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}]}, {'@count': '587', '@count_eth_dst': '373', '@count_eth_src': '214', '@count_ip_dst': '373', '@count_ip_src': '214', '@count_tcp_dst': '373', '@count_tcp_src': '206', '@ether': '98:FC:11:50:AF:A4', 'ip': [{'@addr': '52.54.141.132', '@hostname': '', 'port': {'@number': '47873', '@servicename': ''}}, {'@addr': '175.164.192.168', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '173.194.203.188', '@hostname': '', 'port': {'@number': '27668', '@servicename': ''}}, {'@addr': '216.58.195.78', '@hostname': '', 'port': {'@number': '47873', '@servicename': ''}}, {'@addr': '173.194.202.189', '@hostname': '', 'port': {'@number': '47873', '@servicename': ''}}, {'@addr': '216.58.194.206', '@hostname': '', 'port': {'@number': '47873', '@servicename': ''}}, {'@addr': '54.148.159.16', '@hostname': '', 'port': {'@number': '47873', '@servicename': ''}}, {'@addr': '172.217.6.46', '@hostname': '', 'port': {'@number': '47873', '@servicename': ''}}, {'@addr': '75.75.75.75', '@hostname': '', 'port': {'@number': '13568', '@servicename': ''}}, {'@addr': '216.58.192.4', '@hostname': '', 'port': {'@number': '47873', '@servicename': ''}}, {'@addr': '75.75.76.76', '@hostname': '', 'port': [{'@number': '5207', '@servicename': ''}, {'@number': '6743', '@servicename': ''}, {'@number': '6999', '@servicename': ''}, {'@number': '13568', '@servicename': ''}]}]}, {'@count': '110', '@count_eth_dst': '0', '@count_eth_src': '110', '@count_ip_dst': '0', '@count_ip_src': '110', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': '98:FC:11:50:AF:A6', 'ip': {'@addr': '8.130.132.139', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}, {'@count': '18', '@count_eth_dst': '18', '@count_eth_src': '0', '@count_ip_dst': '18', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': '5C:F6:DC:39:57:E5', 'ip': {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}, {'@count': '14', '@count_eth_dst': '14', '@count_eth_src': '0', '@count_ip_dst': '14', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': 'D0:E7:82:F1:90:90', 'ip': {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}, {'@count': '62548', '@count_eth_dst': '48409', '@count_eth_src': '14139', '@count_ip_dst': '48409', '@count_ip_src': '14139', '@count_tcp_dst': '48409', '@count_tcp_src': '14132', '@ether': 'C8:BC:C8:8D:38:F6', 'ip': [{'@addr': '192.168.1.113', '@hostname': '', 'port': [{'@number': '35091', '@servicename': ''}, {'@number': '5632', '@servicename': ''}]}, {'@addr': '56.246.192.168', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}]}, {'@count': '14', '@count_eth_dst': '14', '@count_eth_src': '0', '@count_ip_dst': '14', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': 'E4:F8:EF:BC:36:42', 'ip': {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}, {'@count': '63165', '@count_eth_dst': '14365', '@count_eth_src': '48800', '@count_ip_dst': '14365', '@count_ip_src': '48798', '@count_tcp_dst': '14338', '@count_tcp_src': '48786', '@ether': '74:DF:BF:66:7C:69', 'ip': [{'@addr': '1.1.0.0', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '227.25.27.255', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '1.113.116.223', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '192.168.1.120', '@hostname': '', 'port': [{'@number': '59668', '@servicename': ''}, {'@number': '58528', '@servicename': ''}, {'@number': '39606', '@servicename': ''}, {'@number': '22720', '@servicename': ''}]}, {'@addr': '1.113.0.0', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}, {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}]}, {'@count': '2', '@count_eth_dst': '2', '@count_eth_src': '0', '@count_ip_dst': '2', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': '33:33:00:00:00:FB', 'ip': {'@addr': '179.82.66.192', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}, {'@count': '4', '@count_eth_dst': '4', '@count_eth_src': '0', '@count_ip_dst': '4', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': '00:26:AB:17:A4:6A', 'ip': {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}, {'@count': '14', '@count_eth_dst': '14', '@count_eth_src': '0', '@count_ip_dst': '14', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': '34:E6:AD:BF:EC:53', 'ip': {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}, {'@count': '4', '@count_eth_dst': '4', '@count_eth_src': '0', '@count_ip_dst': '4', '@count_ip_src': '0', '@count_tcp_dst': '4', '@count_tcp_src': '0', '@ether': '01:00:5E:00:00:FB', 'ip': {'@addr': '224.0.0.251', '@hostname': '', 'port': {'@number': '59668', '@servicename': ''}}}, {'@count': '14', '@count_eth_dst': '14', '@count_eth_src': '0', '@count_ip_dst': '14', '@count_ip_src': '0', '@count_tcp_dst': '0', '@count_tcp_src': '0', '@ether': '44:33:4C:07:E9:DD', 'ip': {'@addr': '150.36.48.72', '@hostname': '', 'port': {'@number': '0', '@servicename': ''}}}]}}
        self.ips = set()
        self.ethers = set()
        self.nodes = set()
        self.node_count = 0
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
        self.nodesummary = parse.ParseNodeSummary(node_json=self.node_json)

    def tearDown(self):
        print ("Coming to teardown")
        print ("Len:IP_TO_ENDPOINTS", len(parse.IP_TO_ENDPOINTS))
        print ("Len:MAC_TO_ENDPOINTS", len(parse.MAC_TO_ENDPOINTS))
        print ("Len:NODES", len(parse.NODES))
        self.node_json = None
        self.nodesummary = None
        #parse.MAC_TO_ENDPOINTS = None
        #parse.NODES = None
        #parse.IP_TO_ENDPOINTS = None

    def test_validate_parsing(self):
        print ("parsing: Len:IP_TO_ENDPOINTS", len(parse.IP_TO_ENDPOINTS))
        print ("parsing: Len:MAC_TO_ENDPOINTS", len(parse.MAC_TO_ENDPOINTS))
        print ("parsing: Len:NODES", len(parse.NODES))
        assert(len(parse.IP_TO_ENDPOINTS)==0)
        assert(len(parse.MAC_TO_ENDPOINTS)==0)
        assert(len(parse.NODES)==0)
        self.nodesummary.parse_summary()
        self.assertEqual(len(parse.IP_TO_ENDPOINTS), len(self.ips))
        self.assertListEqual(sorted(parse.IP_TO_ENDPOINTS.keys()), sorted(self.ips))
        self.assertListEqual(sorted([x.lower() for x in parse.MAC_TO_ENDPOINTS.keys()]), sorted(self.ethers))
        #No cloud IPs, since all are tagged to AP -- albeit incorrectly
        cloud_ip_nodes = [node for node in parse.NODES.values() if node.node_type.value == NodeType.CLOUD_IP.value]
        self.assertEqual(len(cloud_ip_nodes), 0)


    def test_validate_ap_is_correctly_tagged(self):
        print ("tagged: Len:IP_TO_ENDPOINTS", len(parse.IP_TO_ENDPOINTS))
        print ("tagged: Len:MAC_TO_ENDPOINTS", len(parse.MAC_TO_ENDPOINTS))
        print ("tagged: Len:NODES", len(parse.NODES))
        phy_addr = PhysicalAddress(phy_address='98:FC:11:50:AF:A4')
        ap_endpoint = EndPoint(phy_address=phy_addr)
        ap_node = Node(endpoints=[ap_endpoint], node_type=NodeType.WIRELESS_ROUTER)
        ap_endpoint.node_id = ap_node.node_id
        parse.MAC_TO_ENDPOINTS[str(phy_addr)] = ap_endpoint
        parse.NODES[ap_node.node_id] = ap_node
        self.nodesummary.parse_summary()
        cloud_ip_nodes = [node for node in parse.NODES.values() if node.node_type.value == NodeType.CLOUD_IP.value]
        self.assertEqual(len(cloud_ip_nodes), 11)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParseNodeSummary)
    unittest.TextTestRunner(verbosity=2).run(suite)
