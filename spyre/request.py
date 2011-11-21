import httplib2
import urllib
import re
from spyre.response import Response


class Request(object):
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

    def host(self, host=None):
        if host is None:
            host = self.env.get('SERVER_NAME', '')
        else:
            self.env['SERVER_NAME'] = host
        return host

    def port(self, port=None):
        if port is None:
            port = self.env.get('SERVER_PORT', 80)
        else:
            self.env['SERVER_PORT'] = port
        return port

    def script_name(self, script_name=None):
        if script_name is None:
            script_name = self.env.get('SCRIPT_NAME', '')
            if script_name == '' and self._path_info_start_with_slash() is False:
                script_name = '/'
        else:
            self.env['SCRIPT_NAME'] = script_name
        return script_name

    def http_host(self):
        host = self.env.get('HTTP_HOST', None)
        if host is None:
            host = ("%s:%i" % (self.host(), self.port()))
        return host

    def scheme(self, scheme=None):
        if scheme is None:
            scheme = self.env.get('spore.url_scheme', 'http')
        else:
            self.env['spore.url_scheme'] = scheme
        return scheme

    def path(self, path_info=None):
        if path_info is None:
            path_info = self.env.get('PATH_INFO', '')
        else:
            self.env['PATH_INFO'] = path_info
        return path_info

    def base(self):
        final_url = ("%s://%s%s%s" % (self.scheme(), self.http_host(), urllib.quote(self.script_name(), '/'), urllib.quote(self.path(), '/')))
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

        path_info = self.path()
        headers = self.env.get('spore.headers', None)
        form_data = self.env.get('spore.form_data', None)

        query_str = None
        form = {}

        #for k, v in izip(params[::2], params[1::2]):

        print params
        max = len(params)
        i = 0
        while i <= (max - 1):
            modified = 0
            k = params[i]
            v = None
            if i < (max - 1):
                i += 1
                v = params[i]

            if path_info and v:
                (path_info, changes) = re.subn(re.compile(":%s" %k), v, path_info)
                if changes:
                    modified = 1
                    i += 1
                    continue

            if query_str is None:
                query_str = "%s" % k
            else:
                query_str = "%s&%s" % (query_str, k)

            if v:
                query_str = "%s=%s" % (query_str, v)

            i += 1

        path_info = re.sub(":\w+", '', path_info)
        self.path(path_info)

        if query_str is not None:
            self.env['QUERY_STRING'] = query_str

    def _execute_http_request(self, final_url):
        h = httplib2.Http(disable_ssl_certificate_validation=True)
        headers, content = h.request(final_url, self.env.get('REQUEST_METHOD'))

        status = headers['status']
        del headers['status']
        http_response = Response(self.env, status, headers, content)

        return http_response
