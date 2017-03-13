#!/usr/bin/env python3

import dobby.utils.util as util

import unittest
__author__ = """\n""".join(['Vivek Shrivastava (vivek@obiai.tech)'])

class TestUtils(unittest.TestCase):
    def test_get_float_value_returns_floats(self):
        x = {'a':1}
        self.assertEqual(util.get_float_value(x, 'a'), 1.0)
        x = {'a':1.1111}
        self.assertEqual(util.get_float_value(x, 'a'), 1.1111)
        x = {'a':-1.1111}
        self.assertEqual(util.get_float_value(x, 'a'), -1.1111)

    def test_get_float_value_returns_none_on_invalid_input(self):
        x = {'a':'b'}
        self.assertIsNone(util.get_float_value(x, 'a'))
        x = {'a':1}
        self.assertIsNone(util.get_float_value(x, 'b'))
        x = None
        self.assertIsNone(util.get_float_value(x, 'b'))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    unittest.TextTestRunner(verbosity=2).run(suite)

