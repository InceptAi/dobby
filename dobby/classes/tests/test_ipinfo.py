#!/usr/bin/env python3

from dobby.classes.endpoint import *
from dobby.classes.phymodel import *
from dobby.classes.node import *
from dobby.classes.ipinfo import *
from ipaddress import IPv4Address, IPv6Address
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestIPInfo(unittest.TestCase):
    def setUp(self):
        self.ipv4address = IPv4Address('192.168.1.1')
        self.ipv6address = IPv6Address('2001:db8::1000')
        self.hostname = 'youtube.com'
        self.ip_info = IPInfo(ipv4address=self.ipv4address,
                              ipv6address=self.ipv6address,
                              hostname=self.hostname)

    def tearDown(self):
        self.ip_info = None

    def test_validate_filled_endpoint(self):
        self.assertEqual(self.ip_info.ipv4address, self.ipv4address)
        self.assertEqual(self.ip_info.ipv6address, self.ipv6address)
        self.assertEqual(self.ip_info.hostname, self.hostname)
        self.assertIsNone(self.ip_info.gwv4address)
        self.assertIsNone(self.ip_info.gwv6address)

    def test_validate_empty_ip_info(self):
        self.ip_info = IPInfo()
        self.assertIsNone(self.ip_info.ipv4address)
        self.assertIsNone(self.ip_info.ipv6address)
        self.assertIsNone(self.ip_info.hostname)
        self.assertIsNone(self.ip_info.gwv4address)
        self.assertIsNone(self.ip_info.gwv6address)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIPInfo)
    unittest.TextTestRunner(verbosity=2).run(suite)