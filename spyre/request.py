import http
import re
from itertools import izip


class Request(object):

    def __init__(self, env):
        self.env = env
        self.scheme = self.env.get('spore.url_scheme', 'http')
        self.port = self.env.get('SERVER_PORT', '80')
        self.path = self.env.get('PATH_INFO', '')
        self.method = self.env.get('REQUEST_METHOD')
        self._build_url()

    @property
    def host(self):
        host = self.env.get('HTTP_HOST', None)
        if host is None:
            host = self.env.get('SERVER_NAME', '')
        return host

    @property
    def uri_base(self):
        return str(self.url)

    @property
    def script_name(self):
        script_name = self.env.get('SCRIPT_NAME', None)

        if script_name is None or script_name == '':
            script_name = '/'
        return script_name

    def __call__(self):
        # XXX rework this part
        self._expand()
        self.url.path.append(self.path)
        self._query_path()
        # TODO headers etc
        request = http.Request(self.method, str(self.url))
        return request

    def _build_url(self):
        # TODO username password query params
        self.url = http.Url(
            scheme=self.scheme,
            host=self.host,
            port=self.port,
            path=self.script_name,
        )

    def _query_path(self):
        query_string = self.env.get('QUERY_STRING', None)
        if query_string is not None:
            self.url.query = query_string

    def _expand(self):
        params = self.env.get('spore.params', None)

        if params is None:
            return

        path_info = self.path
#        headers = self.env.get('spore.headers', None)
#        form_data = self.env.get('spore.form_data', None)

        query = []
#        form = {}
#        headers = []

        for k, v in izip(params[::2], params[1::2]):
            if path_info:
                (path_info, changes) = re.subn(re.compile(":%s" % k), v, path_info)
                if changes:
                    continue

            query.append((k, v))

        path_info = re.sub(":\w+", '', path_info)
        self.path = path_info

        # TODO check what can be moved to Uri
        if query:
            self.env['QUERY_STRING'] = query
