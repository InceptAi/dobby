#!/usr/bin/env python3

import dobby.utils.util as util

import io
import json
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

    def test_read_json_works_for_valid_json(self):
        json_to_read = dict(a=1)
        input_file_stream = io.StringIO(json.dumps(json_to_read))
        self.assertEqual(util.read_json(input_file_stream), json_to_read)

    def test_read_json_works_for_valid_json(self):
        input_file_stream = io.StringIO('invalid_json')
        self.assertIsNone(util.read_json(input_file_stream))

    def test_read_json_from_file_raises_error_if_no_file(self):
        self.assertIsNone(util.read_json_from_file('fileisnothere'))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
    unittest.TextTestRunner(verbosity=2).run(suite)

