from unittest2 import TestCase
from spyre import Spyre
import spyre.middleware
import spyre.middleware.runtime
import os.path


MY_DIR = os.path.dirname(__file__)
spec = MY_DIR + "/specs/api.json"


class TestSpyreMiddlewareRuntime(TestCase):

    def test_simple(self):
        base_url = 'http://github.com/api/v2/'
        spore = Spyre().new_from_spec(spec, base_url)
        spore.enable('runtime')
        spore.get_user_info({'user': 'foo'})
        self.assertTrue(False)
