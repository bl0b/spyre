from unittest2 import TestCase
from spyre import Spyre
import os.path


MY_DIR = os.path.dirname(__file__)
spec = MY_DIR + "/specs/api.json"


class TestSpyre(TestCase):

    def test_without_spec(self):
        self.assertRaises(RuntimeError, Spyre.new_from_spec, ('spec'))

    def test_create_from_spec(self):
        spore = Spyre().new_from_spec(spec) 
        self.assertTrue(spore)
        self.assertEqual(spore.name, "Test API")
        self.assertEqual(spore.get_info({}), 5)
