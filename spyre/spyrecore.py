import __future__
import re
from spyre import errors


class spyrecore(object):
    def __init__(self, json):
        self.json = json
        self._init_meta(json)
        self._init_methods(json)

    def _init_meta(self, json):
        self.name = json['name']

    def _init_methods(self, json):
        for method_name, method_desc in json['methods'].iteritems():
            self._attach_method(method_name, method_desc)

    def _attach_method(self, method_name, method_desc):
        setattr(self, method_name, spyremethod(method_name, method_desc))


class spyremethod(object):
    def __init__(self, name, desc):
        self.name = name

        if 'method' not in desc:
            raise errors.SpyreMethodBuilder('path')

        self.method = desc['method']
        self.path = desc['path']

    def __call__(self, args):

        payload = self._build_payload(args)

        # XXX build url
        base_url = self._base_url()
        # XXX build auth
        auth = self._build_auth()
        params = self._build_params()
        formats = self._build_formats()
        env = {
                'REQUEST_METHOD': self.method,
                'SERVER_NAME': base_url,
                'SERVER_PORT': base_url,
                'SCRIPT_NAME': base_url,
                'PATH_INFO': self.path,
                'REQUEST_URI': '',
                'QUERY_STRING': '',
                'HTTP_USER_AGENT': '',
                'spore.expected_status': '',
                'spore.authentication': auth,
                'spore.params': params,
                'spore.payload': payload,
                'spore.errors': '',
                'spore.url_scheme': base_url,
                'spore.userinfo': base_url,
                'spore.formats': formats,
                }
        return 5

    def _build_auth(self):
        pass

    def _base_url(self):
        pass

    def _build_params(self):
        pass

    def _build_formats(self):
        pass

    def _build_payload(self, args):
        payload = None
        if 'spore_payload' in args:
            payload = args['spore_payload']
            #delete args['spore_payload']
        elif 'payload' in args:
            payload = args['payload']
            #delete args['payload']

        if payload and re.match(r"^P(OS|U)T$"):
            raise "NON"

        return payload
