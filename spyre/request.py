import httplib2
import urllib
import re
from spyre.response import Response
from itertools import izip


def _requestproperty(key, default=None):

    def fget(self):
        return self.env.get(key, default)

    def fset(self, value):
        self.env[key] = value
        return value

    return property(fget, fset)


class Request(object):

    port = _requestproperty('SERVER_PORT', 80)
    host = _requestproperty('SERVER_NAME', '')
    path = _requestproperty('PATH_INFO', '')
    scheme = _requestproperty('spore.url_scheme', 'http')

    def __init__(self, env):
        self.env = env

    def execute(self):
        final_url = self._finalize()
        http_response = self._execute_http_request(final_url)
        return http_response

    def _finalize(self):
        self._expand()
        final_url = self.base()
        query_string = self.env.get('QUERY_STRING', None)
        if query_string is not None:
            final_url = "%s?%s" % (final_url, query_string)
        return final_url

    @property
    def script_name(self):
        script_name = self.env.get('SCRIPT_NAME', '')
        if script_name == '' and self._path_info_start_with_slash() is False:
            script_name = '/'
        return script_name

    @property
    def http_host(self):
        host = self.env.get('HTTP_HOST', None)
        if host is None:
            host = ("%s:%i" % (self.host, self.port))
        return host

    def base(self):
        final_url = ("%s://%s%s%s" % (self.scheme, self.http_host,
            urllib.quote(self.script_name, '/'), urllib.quote(self.path, '/')))
        return final_url

    def _path_info_start_with_slash(self):
        path_info = self.env.get('PATH_INFO', None)
        if path_info is not None and len(path_info) > 0 and path_info[0] == '/':
            return True
        else:
            return False

    def _expand(self):
        params = self.env.get('spore.params', None)

        if params is None:
            return

        path_info = self.path
        headers = self.env.get('spore.headers', None)
        form_data = self.env.get('spore.form_data', None)

        query = []
        form = {}
        headers = []

        for k, v in izip(params[::2], params[1::2]):
            if path_info:
                (path_info, changes) = re.subn(re.compile(":%s" % k), v, path_info)
                if changes:
                    continue

            query.append("%s=%s" % (k,v))

        path_info = re.sub(":\w+", '', path_info)
        self.path = path_info

        if query:
            self.env['QUERY_STRING'] = '&'.join(query)

    def _execute_http_request(self, final_url):
        h = httplib2.Http(disable_ssl_certificate_validation=True)
        headers, content = h.request(final_url, self.env.get('REQUEST_METHOD'))

        status = headers['status']
        del headers['status']
        http_response = Response(self.env, status, headers, content)

        return http_response
