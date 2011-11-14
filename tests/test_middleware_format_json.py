from unittest2 import TestCase
from spyre import Spyre
import spyre.middleware
import spyre.middleware.formatjson
import os.path


MY_DIR = os.path.dirname(__file__)
spec = MY_DIR + "/specs/api.json"


class TestSpyreMiddlewareFormatJSON(TestCase):

    def test_simple(self):
        spore = Spyre().new_from_spec(spec)
        spore.enable('formatjson')
        resp = spore.get_user_info(username='franckcuny')
        self.assertEqual(resp.content['name'], 'franck')
