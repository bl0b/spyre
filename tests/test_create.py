from unittest2 import TestCase
from spyre import new_from_spec, new_from_string
from spyre.core import Spore
from http import Response
from spyre import errors
import os.path

MY_DIR = os.path.dirname(__file__)
spec_file = MY_DIR + "/specs/api.json"
base_url = 'http://api.github.com/v2/'


class TestSpyre(TestCase):

    def test_without_base_url_as_arguement(self):
        spore = new_from_spec(spec_file)
        self.assertTrue(spore)
        self.assertEqual(spore.base_url, "https://api.github.com/")

    def test_without_spec(self):
        self.assertRaises(errors.SpyreObjectBuilder, new_from_string, ('spec'))

    def test_new_from_spec(self):
        spore = new_from_spec(spec_file, base_url)

        self.assertTrue(spore)
        self.assertEqual(spore.base_url, base_url)
        self.assertEqual(spore.name, "Test API")

        resp = spore.get_user_info(username='franckcuny')
        self.assertIsInstance(resp, Response)

    def test_new_from_string(self):
        f = open(spec_file, 'r')
        spec_str = f.read()
        f.close()
        spore = new_from_string(spec_str)
        self.assertTrue(spore)
        self.assertIsInstance(spore, Spore)

    def test_inexisting_spec(self):
        self.assertRaises(errors.SpyreObjectBuilder, new_from_spec, ('foo'))