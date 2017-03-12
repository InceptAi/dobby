#!/usr/bin/env python3

import dobby.nwmodel.phymodel as phymodel
import unittest
from collections import Counter
__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestWirelessPhyModel(unittest.TestCase):
    def setUp(self):
        self.mac = phymodel.PhysicalAddress(phy_address='AA:BB:CC:DD:EE:FF')
        self.wifi_model = phymodel.WifiPhysicalModel(mac=self.mac, clients=set(), interferers=set())

    def tearDown(self):
        self.wifi_model = None

    def test_wifi_model_is_correctly_instantiated(self):
        self.assertEqual(str(self.wifi_model.mac), 'aa:bb:cc:dd:ee:ff')
        self.assertEqual(self.wifi_model.phy_type, phymodel.PhysicalModelTypes.WIFI)
        self.assertEqual(self.wifi_model.mtu, phymodel.PhysicalLayerMTU.WIFI)
        self.assertEqual(self.wifi_model.clients, set())
        self.assertEqual(self.wifi_model.interferers, set())
        self.assertEqual(self.wifi_model.channel, 0)
        self.assertTrue(isinstance(self.wifi_model, phymodel.WifiPhysicalModel))
        self.assertTrue(isinstance(self.wifi_model, phymodel.PhysicalModel))

    def test_adding_clients_works_properly(self):
        client1 = phymodel.PhysicalAddress(phy_address='11:22:33:44:55:61')
        client2 = phymodel.PhysicalAddress(phy_address='11:22:33:44:55:62')
        client3 = phymodel.PhysicalAddress(phy_address='11:22:33:44:55:61')
        self.wifi_model.add_clients([client1, client2, client3])
        self.assertEqual(self.wifi_model.clients, {client1, client2})

    def test_adding_interferers_works_properly(self):
        interferer1 = phymodel.PhysicalAddress(phy_address='11:22:33:44:55:61')
        interferer2 = phymodel.PhysicalAddress(phy_address='11:22:33:44:55:62')
        interferer3 = phymodel.PhysicalAddress(phy_address='11:22:33:44:55:61')
        self.wifi_model.add_interferers([interferer1, interferer2, interferer3])
        self.assertEqual(self.wifi_model.interferers, {interferer1, interferer2})

    def test_updating_wifi_stats_works(self):
        stats1 = Counter(pkts=10, retx=2)
        stats2 = Counter(pkts=1, retx=1, rate=10)
        self.wifi_model.update_stats(**stats1)
        self.wifi_model.update_stats(**stats2)
        self.assertEqual(self.wifi_model.wifi_stats, Counter(pkts=11, retx=3, rate=10))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWirelessPhyModel)
    unittest.TextTestRunner(verbosity=2).run(suite)
