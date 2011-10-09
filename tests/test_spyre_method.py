from unittest2 import TestCase
from spyre import spyrecore
from spyre import errors


class TestSpyreMethod(TestCase):

    def test_required_attr(self):
        method_name = 'test'
        method_desc = {}

        self.failUnlessRaises(errors.SpyreMethodBuilder,
                spyrecore.spyremethod, method_name,
                method_desc)

        method_desc['method'] = 'GET'
        self.failUnlessRaises(errors.SpyreMethodBuilder,
                spyrecore.spyremethod, method_name,
                method_desc)

        method_desc['path'] = '/:username'
        method = spyrecore.spyremethod(method_name, method_desc)
        self.assertTrue(method)

    def test_optional_attr(self):
        method_name = 'test'
        method_desc = {'method': 'GET', 'path': '/:username',
                'required_params': ['username']}

        method = spyrecore.spyremethod(method_name, method_desc)
        self.assertTrue(method)

        self.failUnlessRaises(errors.SpyreMethodCall, method, {})

    def test_callable(self):
        pass