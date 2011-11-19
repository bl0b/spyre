import __future__
import re
from urlparse import urlparse
from spyre import errors
from spyre.request import Request


class Method(object):
    def __init__(self, name, desc, spore_obj):
        self.name = name
        self.spore_obj = spore_obj
        self.middlewares = []

        self.path = None
        self.method = None
        self.description = None
        self.base_url = None

        self.required_payload = False
        self.authentication = False

        self.formats = []
        self.headers = []
        self.required_params = []
        self.optional_params = []
        self.expected_status = []

        self.base_url = desc.get('base_url', self.spore_obj.base_url)

        self._init_args(desc)

    def _init_args(self, desc):

        required_attr = ['method', 'path']
        optional_attr = [
            'required_params',
            'optional_params',
            'expected_status',
        ]

        for attr in required_attr:
            if attr not in desc:
                raise errors.SpyreMethodBuilder(attr)
            setattr(self, attr, desc[attr])

        for attr in optional_attr:
            if attr in desc:
                setattr(self, attr, desc[attr])

    def __call__(self, **kwargs):

        if self.base_url is None:
            raise errors.SpyreMethodCall("meh")

        cb_response = []

        payload = self._build_payload(kwargs)
        params = self._build_parameters(kwargs)

        auth = self._build_auth()
        formats = self._build_formats()

        base_url = urlparse(self.base_url)

        if base_url.path == '/':
            script_name = ''
        else:
            script_name = base_url.path

        if base_url.username is not None:
            userinfo = ('%s:%s' % (base_url.username, base_url.password))
        else:
            userinfo = None

        if base_url.port is None:
            if base_url.scheme == 'http':
                port = 80
            elif base_url.scheme == 'https':
                port = 443
            else:
                raise "houla"
        else:
            port = base_url.port

        env = {
            'REQUEST_METHOD': self.method,
            'SERVER_NAME': base_url.hostname,
            'SERVER_PORT': port,
            'SCRIPT_NAME': script_name,
            'PATH_INFO': self.path,
            'REQUEST_URI': '',
            'QUERY_STRING': '',
            'HTTP_USER_AGENT': 'spyre',
            'spore.expected_status': self.expected_status,
            'spore.authentication': auth,
            'spore.params': params,
            'spore.payload': payload,
            'spore.errors': '',
            'spore.url_scheme': base_url.scheme,
            'spore.userinfo': userinfo,
            'spore.formats': formats,
        }

        for mw in self.spore_obj.middlewares:
            if mw[0](env):
                cb = mw[1](env)
                if cb:
                    cb_response.append(cb)

        http_response = Request(env).execute()

        if self.expected_status:
            http_status = int(http_response.status)
            request_pass = False
            for exp_status in self.expected_status:
                if exp_status == http_status:
                    request_pass = True
            if request_pass is False:
                raise errors.SpyreStatusInvalid()

        for cb in cb_response:
            cb(http_response)

        return http_response

    def _build_parameters(self, kwargs):
        kset = set(kwargs.iterkeys())
        required = set(self.required_params)
        optional = set(self.optional_params)
        params = required.union(optional)

        stuff_remains = kset.difference(
            self.required_params + self.optional_params)
        if stuff_remains:
            raise errors.SpyreMethodCall(stuff_remains)

        missing_req = required.difference(kset)
        if missing_req:
            raise errors.SpyreMethodCall(missing_req)

        arg_dic = kwargs
        return arg_dic

    def _build_auth(self):
        pass

    def _base_url(self):
        pass

    def _build_formats(self):
        pass

    def _build_payload(self, args):
        payload = None
        payload = args.get('spore_payload', 'payload')

        if payload is None and self.required_payload:
            raise errors.SpyreMethodPayloadRequired()

        if payload is None:
            return

        # XXX delete payload param from args
        # XXX add support for PATCH ? (same for N::H::Spore)
        if payload and re.match(r"^P(OS|U)T$", payload):
            raise errors.SpyreMethodPayload()

        return payload
