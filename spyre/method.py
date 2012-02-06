import __future__
import re
from http import Url
from spyre import errors
from spyre.request import Request


class Method(object):

    required_attr = ['method', 'path']
    optional_attr = [
        'required_params',
        'optional_params',
        'expected_status',
    ]

    def __init__(self, name, desc, base_url, user_agent, middlewares=None):
        self.name = name
        self.user_agent = user_agent

        if middlewares is None:
            middlewares = []
        self.middlewares = middlewares

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

        self.base_url = desc.get('base_url', base_url)

        self._init_args(desc)

    def _init_args(self, desc):
        self._required_attributes(desc)
        self._optional_attirbutes(desc)

    def _required_attributes(self, desc):
        for attr in self.required_attr:
            if attr not in desc:
                raise errors.SpyreMethodBuilder(attr)
            setattr(self, attr, desc[attr])

    def _optional_attirbutes(self, desc):
        for attr in self.optional_attr:
            if attr in desc:
                setattr(self, attr, desc[attr])

    def _script_name(self, base_url):
        if base_url.path == '/':
            return ''
        else:
            return base_url.path

    def _userinfo(self, base_url):
        if base_url.username is not None:
            return ('%s:%s' % (base_url.username, base_url.password))
        else:
            return None

    def _port(self, base_url):
        if base_url.port is not None:
            return base_url.port

        if base_url.scheme == 'http':
            return 80
        elif base_url.scheme == 'https':
            return 443
        else:
            raise "houla"

    def __call__(self, **kwargs):

        if self.base_url is None:
            raise errors.SpyreMethodCall("`base_url` is missing")

        cb_response = []

        payload = self._build_payload(kwargs)
        params = self._build_parameters(kwargs)

        auth = self._build_auth()
        formats = self._build_formats()

        base_url = Url(string_url=self.base_url)

        script_name = self._script_name(base_url)
        userinfo = self._userinfo(base_url)
        port = self._port(base_url)

        env = {
            'REQUEST_METHOD': self.method,
            'SERVER_NAME': base_url.netloc,
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

        for mw in self.middlewares:
            if mw[0](env):
                cb = mw[1](env)
                if cb:
                    cb_response.append(cb)

        request = Request(env)
        http_response = self.user_agent.request(request())
        setattr(http_response, 'env', env)

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

        params = []
        for k,v in kwargs.iteritems():
            params.append(k)
            params.append(v)
        return params

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
