from unittest2 import TestCase
from spyre import Spyre
from spyre.response import Response
from spyre import errors
import os.path

MY_DIR = os.path.dirname(__file__)
spec_file = MY_DIR + "/specs/api.json"
base_url = 'http://api.github.com/v2/'


class TestSpyre(TestCase):

    def test_without_base_url_as_arguement(self):
        spore = Spyre().new_from_spec(spec_file)
        self.assertTrue(spore)
        self.assertEqual(spore.base_url, "https://api.github.com/")

    def test_without_spec(self):
        self.assertRaises(errors.SpyreObjectBuilder, Spyre.new_from_string, ('spec'))

    def test_new_from_spec(self):
        spore = Spyre().new_from_spec(spec_file, base_url)
        self.assertTrue(spore)
        self.assertEqual(spore.name, "Test API")
        resp = spore.get_user_info(username='franckcuny')
        self.assertIsInstance(resp, Response)

        spore = Spyre().new_from_spec(spec_file, base_url)
        self.assertTrue(spore)

    def test_new_from_string(self):
        f = open(spec_file, 'r')
        spec_str = f.read()
        f.close()
        spore = Spyre().new_from_string(spec_str, base_url)
        self.assertTrue(spore)