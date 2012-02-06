from unittest2 import TestCase
from spyre import new_from_spec
import os.path

MY_DIR = os.path.dirname(__file__)
spec = MY_DIR + "/specs/api.json"


class TestSpyreMiddlewareFormatJSON(TestCase):

    def test_simple(self):
        spore = new_from_spec(spec)
        spore.enable('formatjson')
        resp = spore.get_user_info(username='franckcuny')
        content = resp.content
        print content
        self.assertEqual(content['name'], 'franck')
