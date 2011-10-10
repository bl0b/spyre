import httplib2
from spyre import response


class spyrerequest(object):
    def __init__(self, env):
        self.env = env

    def execute(self):
        return self._finalize()

    def _finalize(self):
        final_url = self._construct_url()
        h = httplib2.Http()
        resp, content = h.request(final_url, self.env['REQUEST_METHOD'])
        status = resp['status']
        http_response = response.spyreresponse(self.env, status, resp, content)
        return http_response

    def _construct_url(self):
        final_url = ("%s://%s:%i/%s" % (self.env['spore.url_scheme'],
            self.env['SERVER_NAME'], self.env['SERVER_PORT'],
            self.env['SCRIPT_NAME']))
        return final_url
