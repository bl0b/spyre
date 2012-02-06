from unittest2 import TestCase
from httpclient import HTTPClient
from spyre.method import Method
from spyre.core import Spore
from spyre import errors
import os.path


MY_DIR = os.path.dirname(__file__)
spec_file = MY_DIR + "/specs/api.json"
base_url = 'https://api.github.com/'
f = open(spec_file, 'r')
spec_str = f.read()
f.close()
base = Spore(spec_str, base_url)


class TestSpyreMethod(TestCase):

    def setUp(self):
        self.user_agent = HTTPClient()
        self.url = 'http://github.com/api/v2/json/'

    def test_required_attr(self):
        method_name = 'test'
        method_desc = {}

        self.failUnlessRaises(errors.SpyreMethodBuilder,
                Method, method_name,
                method_desc, base_url=self.url, user_agent=self.user_agent)

        method_desc['method'] = 'GET'
        self.failUnlessRaises(errors.SpyreMethodBuilder,
                Method, method_name,
                method_desc, base_url=self.url, user_agent=self.user_agent)

        method_desc['path'] = '/user/show/:username'
        method_desc['required_params'] = ['username']
        method_desc['expected_status'] = [200, 404, 406]

        method = Method(method_name, method_desc, base_url=self.url, user_agent=self.user_agent)
        self.assertTrue(method)
        resp = method(username='franckcuny')
        print resp.content
        self.assertEqual(resp.status, 200)

    def test_optional_attr(self):
        method_name = 'test'
        method_desc = {'method': 'GET', 'path': '/:username',
                'required_params': ['username']}
        base_url = 'http://github.com/api/v2/'

        method = Method(method_name, method_desc, base_url=self.url, user_agent=self.user_agent)
        self.assertTrue(method)

        self.failUnlessRaises(errors.SpyreMethodCall, method)

    def test_callable(self):
        pass

    def test_payload(self):
        pass
