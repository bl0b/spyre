from unittest2 import TestCase
from spyre import spyrecore
from spyre import errors


class TestSpyreMethod(TestCase):

    def test_errors(self):
        method_desc = {}
        self.failUnlessRaises(errors.SpyreMethodBuilder,
                spyrecore.spyremethod, 'test',
                method_desc)
