from unittest2 import TestCase
from spyre import spyrecore
from spyre import errors


class TestSpyreMethod(TestCase):

    def test_required_attr(self):
        method_name = 'test'
        method_desc = {}
        base_url = 'http://github.com/api/v2/'

        self.failUnlessRaises(errors.SpyreMethodBuilder,
                spyrecore.spyremethod, method_name,
                method_desc, base_url)

        method_desc['method'] = 'GET'
        self.failUnlessRaises(errors.SpyreMethodBuilder,
                spyrecore.spyremethod, method_name,
                method_desc, base_url)

        method_desc['path'] = '/:username'
        method = spyrecore.spyremethod(method_name, method_desc, base_url)
        self.assertTrue(method)
        resp = method({})
        self.assertEqual(resp.status, '404')

    def test_optional_attr(self):
        method_name = 'test'
        method_desc = {'method': 'GET', 'path': '/:username',
                'required_params': ['username']}
        base_url = 'http://github.com/api/v2/'

        method = spyrecore.spyremethod(method_name, method_desc, base_url)
        self.assertTrue(method)

        self.failUnlessRaises(errors.SpyreMethodCall, method, {})

    def test_callable(self):
        pass
