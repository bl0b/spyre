import __future__
import re
from urlparse import urlparse
from spyre import errors
from spyre import request


class spyrecore(object):
    def __init__(self, json, base_url):
        self.json = json
        self.base_url = None

        self._init_meta(json, base_url)

        self._init_methods(json)

    def _init_meta(self, json, base_url):
        self.name = json['name']

        if 'base_url' in json:
            self.base_url = json['base_url']
        elif base_url is not None:
            self.base_url = base_url
        else:
            raise "NON"

    def _init_methods(self, json):
        for method_name, method_desc in json['methods'].iteritems():
            self._attach_method(method_name, method_desc)

    def _attach_method(self, method_name, method_desc):
        setattr(self, method_name, spyremethod(method_name, method_desc,
            self.base_url))


class spyremethod(object):
    def __init__(self, name, desc, base_url):
        self.name = name

        self.method = None
        self.path = None
        self.base_url = None
        self.required_params = []
        self.optional_params = []

        if 'base_url' in desc:
            self.base_url = desc['base_url']
        else:
            self.base_url = base_url

        self._init_args(desc)

    def _init_args(self, desc):

        required_attr = ['method', 'path']
        optional_attr = ['required_params', 'optional_params']

        for attr in required_attr:
            if attr not in desc:
                raise errors.SpyreMethodBuilder(attr)
            setattr(self, attr, desc[attr])

        for attr in optional_attr:
            if attr in desc:
                setattr(self, attr, desc[attr])

    def __call__(self, args):

        payload = self._build_payload(args)

        self._check_required_params(args)

        base_url = urlparse(self.base_url)

        # XXX build auth
        auth = self._build_auth()
        params = self._build_params()
        formats = self._build_formats()

        env = {
                'REQUEST_METHOD': self.method,
                'SERVER_NAME': base_url.hostname,
                'SERVER_PORT': base_url.port,
                'SCRIPT_NAME': base_url.path,
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

        http_response = request.spyrerequest(env)
        print http_response
        #my $code = $response->status;

        #my $ok = ($method->has_expected_status)
            #? $method->find_expected_status( sub { $_ eq $code } )
            #: $response->is_success; # only 2xx is success
        #die $response if not $ok;

        #$response;
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
            raise errors.SpyreMethodPayload()

        # XXX check if payload is required

        return payload

    def _check_required_params(self, args):
        if len(self.required_params) < 1:
            return

        for param in self.required_params:
            if param not in args:
                raise errors.SpyreMethodCall(param)
