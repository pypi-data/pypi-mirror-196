from __future__ import absolute_import
from __future__ import unicode_literals

import unittest
import os
from laipvt.sysutil.util import *


current_path = os.path.dirname(os.path.abspath(__file__))

class TestUtil(unittest.TestCase):

    def test_to_object(self):
        d = {
            'foo': [
                {
                    'a': 1,
                    'b': {
                        'c': 2,
                    }
                }
            ],
            'bar': 5
        }
        obj = to_object(d)
        self.assertEqual(obj.foo[0].a, 1)
        self.assertEqual(obj.foo[0].b.c, 2)
        self.assertEqual(obj.bar, 5)
        obj.bar = 100
        self.assertEqual(obj.bar, 100)
        self.assertEqual(d['bar'], 5)
        obj.foo[0].a = False
        self.assertFalse(obj.foo[0].a)
        self.assertTrue(d['foo'][0]['a'])

    def test_get_yaml_config(self):
        cfg = get_yaml_config(os.path.join(current_path, "test_files/test.yaml"))
        self.assertEqual(cfg["a"], 1)
        self.assertTrue(cfg["b"])
        self.assertEqual(cfg["c"], "foo")

    def test_get_json_config(self):
        cfg = get_json_config(os.path.join(current_path, "test_files/test.json"))
        self.assertEqual(cfg["a"], 1)
        self.assertTrue(cfg["b"])
        self.assertEqual(cfg["c"], "foo")

    def test_get_yaml_obj(self):
        cfg = get_yaml_obj(os.path.join(current_path, "test_files/test.yaml"))
        self.assertEqual(cfg.a, 1)
        self.assertTrue(cfg.b)
        self.assertEqual(cfg.c, "foo")

if __name__ == '__main__':
    unittest.main()