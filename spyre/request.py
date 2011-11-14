import httplib2
from spyre.response import Response


class Request(object):
    def __init__(self, env):
        self.env = env

    def execute(self):
        self.env['PATH_INFO'] = self.expand('PATH_INFO')
        final_url = self._construct_url()
        http_response = self._execute_http_request(final_url)
        return http_response

    def _construct_url(self):
        final_url = ("%s://%s:%i%s" % (self.env['spore.url_scheme'],
            self.env['SERVER_NAME'], self.env['SERVER_PORT'],
            self.env['SCRIPT_NAME']))

        path_info = self.env.get('PATH_INFO');
        final_url = ('%s%s' % (final_url, path_info))

        return final_url

    def expand(self, key_name):
        dic = self.env.get('spore.params')
        txt = self.env.get(key_name)
        for k, v in dic.iteritems():
            txt = v.join(txt.split(':'+k))
        return txt

    def _execute_http_request(self, final_url):
        h = httplib2.Http(disable_ssl_certificate_validation=True)
        resp, content = h.request(final_url, self.env.get('REQUEST_METHOD'))

        status = resp['status']
        http_response = Response(self.env, status, resp, content)

        return http_response

