#!/usr/bin/env python3

import dobby.nwmetrics.metrics as metrics
import unittest

__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])


class TestStats(unittest.TestCase):
    def setUp(self):
        self.stats = metrics.Stats(min_val=10.254, max_val=120.001, num_samples=10)

    def tearDown(self):
        self.stats = None

    def test_validate_stats(self):
        #rtt stats
        self.assertEqual(self.stats.min_val, 10.254)
        self.assertEqual(self.stats.max_val, 120.001)
        self.assertEqual(self.stats.num_samples, 10)

    def test_stats_eq_works(self):
        #rtt stats
        stats1 = metrics.Stats(min_val=10.254, max_val=120.001, num_samples=10)
        stats2 = dict(min_val=10.254, max_val=120.001, num_samples=10)
        self.assertEqual(self.stats, stats1)
        self.assertNotEqual(self.stats, stats2)

    def test_stats_ne_works(self):
        #rtt stats
        stats1 = metrics.Stats(min_val=10.254, max_val=120.001, num_samples=11)
        self.assertNotEqual(self.stats, stats1)

    def test_stats_returns_none_on_none_string(self):
        self.assertIsNone(metrics.Stats.from_string(value_string=None))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStats)
    unittest.TextTestRunner(verbosity=2).run(suite)
