from unittest2 import TestCase
from spyre import spyrecore
from spyre import errors
from spyre.request import Request
import yaml
import os.path


MY_DIR = os.path.dirname(__file__)

class TestSpyreRequest(TestCase):

    def _get_test_data(self, fname):
        file = MY_DIR + "/data/" + fname + ".yaml"
        f = open(file)
        test_data = yaml.load(f)
        f.close()
        return test_data

    def test_create_base_url(self):
        test_data_url = self._get_test_data('base_url')

        for test in test_data_url:
            env = {
                'spore.url_scheme': test.get('scheme', 'http'),
                'HTTP_HOST': test.get('host', None),
                'SERVER_NAME': test.get('server_name', None),
                'SERVER_PORT': test.get('server_port', None),
                'SCRIPT_NAME': test.get('script_name', ''),
            }
            request = Request(env)
            self.assertEqual(request.base(), test['base'])

    def test_populate_uri(self):
        test_data_url = self._get_test_data('uri')

        for test in test_data_url:
            env = {
                'SERVER_PORT': 80
            }
            if test.get('add_env', None) is not None:
                for k,v in test['add_env'].iteritems():
                    env[k] = v
            req = Request(env)
            self.assertEqual(req._finalize(), test['uri'])

    #def test_populate_headers(self):
        #test_data_headers = self._get_test_data('headers')

        #for test in test_data_headers:
            #req = Request(env)
            #req._finalize()
