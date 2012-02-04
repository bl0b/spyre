from unittest2 import TestCase
import spyre.core
from spyre import errors
from spyre.response import Response


env = {
    'HTTP_METHOD': 'GET',
}

headers = {
    'content-type': 'text/html',
    'content-length': 3,
}

body = 'foo'
        
class TestSpyreResponse(TestCase):

    def test_create_basic_response(self):
        spyre_response = Response(env, 200)
        self.assertEqual(spyre_response.status, 200)
        self.assertEqual(spyre_response.code, 200)
        self.assertTrue(spyre_response.is_success)

    def test_create_with_resp(self):
        spyre_response = Response(env, 200, headers, body)
        self.assertEqual(spyre_response.content_type, 'text/html')
        self.assertEqual(spyre_response.content_length, 3)
        self.assertEqual(spyre_response.content, 'foo')
 
    def test_response_header(self):
        spyre_response = Response(env, 200, headers, body)
        self.assertEqual(spyre_response.header('content-type'), 'text/html')
        
    def test_response_headers(self):
        spyre_response = Response(env, 200, headers, body)
        resp_headers = spyre_response.headers()
        self.assertTrue('content-type' in resp_headers)