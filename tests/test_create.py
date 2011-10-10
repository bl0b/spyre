from unittest2 import TestCase
from spyre import Spyre
from spyre import response
import os.path


MY_DIR = os.path.dirname(__file__)
spec = MY_DIR + "/specs/api.json"


class TestSpyre(TestCase):

    def test_without_spec(self):
        self.assertRaises(RuntimeError, Spyre.new_from_spec, ('spec'))

    def test_create_without_base_url(self):
        # XXX
        pass

    def test_create_from_spec(self):
        base_url = 'http://github.com/api/v2/'
        spore = Spyre().new_from_spec(spec, base_url) 
        self.assertTrue(spore)
        self.assertEqual(spore.name, "Test API")
        resp = spore.get_info({})
        self.assertIsInstance(resp, response.spyreresponse)
