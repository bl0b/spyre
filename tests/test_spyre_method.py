from unittest2 import TestCase
from spyre.method import Method
from spyre.core import base
from spyre import errors
import os.path


MY_DIR = os.path.dirname(__file__)
spec_file = MY_DIR + "/specs/api.json"
base_url = 'http://github.com/api/v2'
f = open(spec_file, 'r')
spec_str = f.read()
f.close()
base = base(spec_str, base_url)

class TestSpyreMethod(TestCase):

    def test_required_attr(self):
        method_name = 'test'
        method_desc = {}

        self.failUnlessRaises(errors.SpyreMethodBuilder,
                Method, method_name,
                method_desc, base)

        method_desc['method'] = 'GET'
        self.failUnlessRaises(errors.SpyreMethodBuilder,
                Method, method_name,
                method_desc, base)

        method_desc['path'] = '/user/:username'
        method_desc['required_params'] = ['username']
        method_desc['expected_status'] = [200, 404, 406]

        method = Method(method_name, method_desc, base)
        self.assertTrue(method)
        resp = method(username='bar')
        self.assertEqual(resp.status, '406')
	self.assertTrue(False)

    def test_optional_attr(self):
        method_name = 'test'
        method_desc = {'method': 'GET', 'path': '/:username',
                'required_params': ['username']}
        base_url = 'http://github.com/api/v2/'

        method = Method(method_name, method_desc, base)
        self.assertTrue(method)

        self.failUnlessRaises(errors.SpyreMethodCall, method)

    def test_callable(self):
        pass

    def test_payload(self):
        pass
